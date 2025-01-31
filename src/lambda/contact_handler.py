import boto3
import os
import json
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from botocore.exceptions import ClientError
import logging
import sys

# UTF-8をデフォルトのエンコーディングに設定
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
ses = boto3.client('ses', region_name='ap-northeast-1')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
SES_SOURCE_EMAIL = "no-reply@00704.engineed-exam.com"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))
    try:
        body = json.loads(event['body'])
        email = body['email']
        last_name = body['last_name']
        first_name = body['first_name']
        inquiry_content = body['inquiry_content']

        inquiry_id = str(uuid.uuid4())
        created_at = datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()

        table = dynamodb.Table(TABLE_NAME)
        response = table.put_item(
            Item={
                'inquiry_id': inquiry_id,
                'email': email,
                'last_name': last_name,
                'first_name': first_name,
                'inquiry_content': inquiry_content.encode('utf-8').decode('utf-8'),
                'created_at': created_at
            }
        )
        print("DynamoDB書き込み成功:", response)

        email_response = ses.send_email(
            Source=SES_SOURCE_EMAIL,
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': '問い合わせ受付完了',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': f"以下の問い合わせを受け付けました:\n\n"
                                f"ID: {inquiry_id}\n"
                                f"Email: {email}\n"
                                f"Last Name: {last_name}\n"
                                f"First Name: {first_name}\n"
                                f"Inquiry Content: {inquiry_content}\n\n"
                                f"このメールは送信専用ですので、返信はできません。",
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        print("SESメール送信成功:", email_response)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': '問い合わせを受け付けました', 'inquiry_id': inquiry_id}, ensure_ascii=False)
        }

    except ClientError as e:
        print("エラーが発生しました:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False)
        }
