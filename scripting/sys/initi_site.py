import argparse
from scripting.loader.models import site 
from scripting.sys.aws_initialization import *

BUCKET_NAME = 'more-jobs'

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
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/placement")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/page")
    
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/placement/response_data")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/placement/parsed_data")
    
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/page/response_data")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/page/parsed_data")

    return {
        's3_placement_response_data': f"s3://{BUCKET_NAME}/{config_data['site']}/placement/response_data",
        's3_placement_parsed_data': f"s3://{BUCKET_NAME}/{config_data['site']}/placement/parsed_data",
        's3_page_response_data': f"s3://{BUCKET_NAME}/{config_data['site']}/page/response_data",
        's3_page_parsed_data': f"s3://{BUCKET_NAME}/{config_data['site']}/page/parsed_data",
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

def create_docker_image_placement(config_data):
    pass

def create_docker_image_crawler(config_data):
    pass
    
if __name__ == "__main__":
    arg_page = argparse.Argumentpage(description="Parase arguemtn for init_site script")
    arg_page.add_argument("--site_name")
    args = arg_page.parse_args()
    
    # site_config = read_yaml(args.site_name)

    
    
    
    
