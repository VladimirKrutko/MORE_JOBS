from dotenv import load_dotenv
import boto3
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'eu-central-1')
BUCKET_NAME = 'more-jobs-2'
SITE_TABLE = boto3.resource('dynamodb', region_name='eu-central-1').Table('site-data')
PLACEMENT_TABLE = boto3.resource('dynamodb', region_name='eu-central-1').Table('placement-data')
PAGE_LOADER_SQS = 'https://sqs.eu-central-1.amazonaws.com/221082168740/page_loader.fifo'
PLACEMENT_LOADER_SQS = 'https://sqs.eu-central-1.amazonaws.com/221082168740/placement_loader.fifo'
SQS_ERORR = 'https://sqs.eu-central-1.amazonaws.com/221082168740/error_queu'
SQS_LOADER = 'https://sqs.eu-central-1.amazonaws.com/221082168740/loader_queue'
SQS_ERORR_LOADER = 'https://sqs.eu-central-1.amazonaws.com/221082168740/loader_error.fifo'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)