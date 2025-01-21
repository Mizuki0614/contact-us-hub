import boto3
import os
import json
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9以降で利用可能
from botocore.exceptions import ClientError

# DynamoDBクライアント
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
# SESクライアント
ses = boto3.client('ses', region_name='ap-northeast-1')

# DynamoDBテーブル名（環境変数で管理）
TABLE_NAME = os.environ['DYNAMODB_TABLE']
# SES送信元（固定）
SES_SOURCE_EMAIL = "no-reply@00704.engineed-exam.com"

def lambda_handler(event, context):
    try:
        # リクエストボディを取得
        body = json.loads(event['body'])
        email = body['email']
        last_name = body['last_name']
        first_name = body['first_name']
        inquiry_content = body['inquiry_content']

        # 一意のIDを生成
        inquiry_id = str(uuid.uuid4())

        # 現在時刻をJSTに変換
        created_at = datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()

        # DynamoDBにデータを書き込む
        table = dynamodb.Table(TABLE_NAME)
        response = table.put_item(
            Item={
                'inquiry_id': inquiry_id,
                'email': email,
                'last_name': last_name,
                'first_name': first_name,
                'inquiry_content': inquiry_content,
                'created_at': created_at
            }
        )
        print("DynamoDB書き込み成功:", response)

        # SESでメールを送信
        email_response = ses.send_email(
            Source=SES_SOURCE_EMAIL,
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': '問い合わせ受付完了'
                },
                'Body': {
                    'Text': {
                        'Data': f"以下の問い合わせを受け付けました:\n\n"
                                f"ID: {inquiry_id}\n"
                                f"Email: {email}\n"
                                f"Last Name: {last_name}\n"
                                f"First Name: {first_name}\n"
                                f"Inquiry Content: {inquiry_content}\n\n"
                                f"このメールは送信専用ですので、返信はできません。"
                        }
                    }
                }
        )
        print("SESメール送信成功:", email_response)

        # レスポンスを返却
        return {
            'statusCode': 200,
            'body': json.dumps({'message': '問い合わせを受け付けました', 'inquiry_id': inquiry_id})
        }

    except ClientError as e:
        print("エラーが発生しました:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Deploy Test