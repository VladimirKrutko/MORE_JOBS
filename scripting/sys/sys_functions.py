from scripting.sys.aws_initialization import session
import json

BACKET_NAME = "more-jobs"
SQS_CLIENT = session.client('sqs')
S3_CLIENT = session.client('s3')

def listeting_sqs(queue_url):
    while True:
        response = SQS_CLIENT.receive_message(
            QueueUrl= queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )
        if 'Messages' in response:
            message = response['Messages'][0]
            return {
                'message': json.loads(message['Body']),
                'message_receipt_handle': message['ReceiptHandle'],
                'message_id': message['MessageId']
            }