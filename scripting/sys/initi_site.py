
import os
import boto3
import argparse
from dotenv import load_dotenv
from .reade_config import read_yaml
from scripting.loader.models import site 

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
BUCKET_NAME = 'more-jobs'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

sqs_client = session.client('sqs')

sqs_attributes = {
    'FifoQueue': 'true',
    'ContentBasedDeduplication': 'true',
    'DelaySeconds': '60',
    'MaximumMessageSize': '262144',
    'MessageRetentionPeriod': '86400',
    'VisibilityTimeout': '60',
    'ReceiveMessageWaitTimeSeconds': '0',
}

def create_s3_buckets(config_data):
    s3_client = session.client('s3')
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/plugin")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/parser")
    
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/plugin/response_data")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/plugin/parsed_data")
    
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/parser/response_data")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/parser/parsed_data")
    return {
        's3_plugin_response_data': f"s3://{BUCKET_NAME}/{config_data['site']}/plugin/response_data",
        's3_plugin_parsed_data': f"s3://{BUCKET_NAME}/{config_data['site']}/plugin/parsed_data",
        's3_parser_response_data': f"s3://{BUCKET_NAME}/{config_data['site']}/parser/response_data",
        's3_parser_parsed_data': f"s3://{BUCKET_NAME}/{config_data['site']}/parser/parsed_data",
    }

def create_table_record(config_data):
    site.Site.create(name=config_data['site'], url=config_data['seed_url'])

def create_queue_sqs(queue_name):
    response = sqs_client.create_queue(
        QueueName= f"{queue_name}.fifo",
        Attributes=sqs_attributes
    )
    return response['QueueUrl']

def creete_docker_image_parse(config_data):
    pass

def create_docker_image_plugin(config_data):
    pass

def create_docker_image_crawler(config_data):
    pass
    
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parase arguemtn for init_site script")
    arg_parser.add_argument("--site_name")
    args = arg_parser.parse_args()
    
    site_config = read_yaml(args.site_name)

    
    
    
    
