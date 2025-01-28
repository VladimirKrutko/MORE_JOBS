from scripting.sys.aws_variables import *
from scripting.loader.models.page_status import PageStatus
import logging
import json
import sys
import re

SQS_CLIENT = session.client('sqs')
S3_CLIENT = session.client('s3')
MESSAGE_GROUP = 'site_crawler'
URL_STATUS = {
    'downloaded': 'downloaded',
    'error': 'error',
    'parsed': 'parsed',
    'saved': 'saved',
}

def upate_page_status(url, status):
    PageStatus.add_or_update_page_status(url, status)

def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message_to_sqs(queue_url, message):
    if '.fifo' in queue_url:
        SQS_CLIENT.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
            MessageGroupId= MESSAGE_GROUP,
        )
    else:
        SQS_CLIENT.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
        )
    logging.info("Send message to SQS: %s", queue_url)

def delete_message_from_sqs(queue_url, receipt_handle):
    SQS_CLIENT.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    logging.info("Delete message from SQS: %s", receipt_handle)

def put_s3_object(data, file_path, content_type='text/html'  ):
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=data, ContentType=content_type)
    logging.info("Put object to S3: %s", file_path)
    return file_path

def read_s3_object(s3_path):
    response = S3_CLIENT.get_object(Bucket=BUCKET_NAME, Key=s3_path)
    return response['Body'].read().decode('utf-8')

def replace_punctuations(text):
    return re.sub(r'[^\w\s]', '_', text)

def create_file_name_from_url(url):
    return  replace_punctuations(url.replace('https://', ''))

def signal_handler(sig, frame):
    logging.info("Stop process")
    sys.exit(0)

def listeting_sqs(queue_url):
    while True:
        logging.info("Listening SQS queue: %s", queue_url)
        response = SQS_CLIENT.receive_message(
            QueueUrl= queue_url,
            MaxNumberOfMessages= 1,
            VisibilityTimeout= 200,
            WaitTimeSeconds= 1,
        )

        if 'Messages' in response:
            message = response['Messages'][0]
            logging.info("Received message: %s", message['MessageId'])
            return {
                'message': json.loads(message['Body'].replace("'", '"')),
                'message_receipt_handle': message['ReceiptHandle'],
                'message_id': message['MessageId']
            }
