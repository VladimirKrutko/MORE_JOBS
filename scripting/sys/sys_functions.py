from scripting.sys.aws_variables import session
import logging
import json

def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BACKET_NAME = "more-jobs"
SQS_CLIENT = session.client('sqs')
S3_CLIENT = session.client('s3')
MESSAGE_GROUP = 'site_crawler'

def send_message_to_sqs(queue_url, message):
    SQS_CLIENT.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        MessageGroupId= MESSAGE_GROUP,
    )
    logging.info("Send message to SQS: %s", queue_url)

def delete_message_from_sqs(queue_url, receipt_handle):
    SQS_CLIENT.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    logging.info("Delete message from SQS: %s", receipt_handle)

def put_s3_object(data, file_name, base_path):
    s3_path = f"{base_path}/{file_name}.json"
    S3_CLIENT.put_object(Bucket=BACKET_NAME, Key=s3_path, Body=json.dumps(data))
    logging.info("Put object to S3: %s", s3_path)
    return s3_path

def read_s3_object(s3_path):
    response = S3_CLIENT.get_object(Bucket=BACKET_NAME, Key=s3_path)
    return response['Body'].read().decode('utf-8')

def listeting_sqs(queue_url):
    while True:
        logging.info("Listening to SQS queue: %s", queue_url)
        response = SQS_CLIENT.receive_message(
            QueueUrl= queue_url,
            MaxNumberOfMessages= 1,
            VisibilityTimeout= 200,
            WaitTimeSeconds= 2,
        )
        
        if 'Messages' in response:
            message = response['Messages'][0]
            logging.info("Received message: %s", message['MessageId'])
            return {
                'message': json.loads(message['Body'].replace("'", '"')),
                'message_receipt_handle': message['ReceiptHandle'],
                'message_id': message['MessageId']
            }
