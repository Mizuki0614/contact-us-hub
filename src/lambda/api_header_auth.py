import json

def lambda_handler(event, context):
    # 期待するカスタムヘッダーの値
    EXPECTED_HEADER_VALUE = "Secret12345"

    # ヘッダーの取得
    headers = event["headers"]
    received_value = headers.get("x-cloudfront-auth", "")

    if received_value == EXPECTED_HEADER_VALUE:
        # 認証成功
        return {
            "principalId": "CloudFrontUser",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": event["methodArn"]
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
                        "Resource": event["methodArn"]
                    }
                ]
            }
        }
