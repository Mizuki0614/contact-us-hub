import json
import boto3
import os

# AWS Systems Manager クライアントを作成
ssm = boto3.client("ssm")

def get_expected_header_value():
    """
    AWS Systems Manager Parameter Store から `EXPECTED_HEADER_VALUE` を取得
    """
    parameter_name = os.getenv("PARAMETER_STORE_KEY", "/contact-api/expected-header-value")
    
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound:
        print(f"ERROR: Parameter {parameter_name} not found.")
        return None

def lambda_handler(event, context):
    expected_header_value = get_expected_header_value()
    
    if expected_header_value is None:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error: Parameter not found"})
        }
    
    # ヘッダーの取得
    headers = event.get("headers", {})
    received_value = headers.get("x-cloudfront-auth", "")

    # HTTP API の場合は `routeArn` を使う
    route_arn = event.get("routeArn", "arn:aws:execute-api::unknown")

    if received_value == expected_header_value:
        # 認証成功
        return {
            "principalId": "CloudFrontUser",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": route_arn  # `methodArn` ではなく `routeArn` を使用
                    }
                ]
            }
        }
    else:
        # 認証失敗（403）
        return {
            "principalId": "UnauthorizedUser",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Deny",
                        "Resource": route_arn  # `methodArn` ではなく `routeArn` を使用
                    }
                ]
            }
        }
