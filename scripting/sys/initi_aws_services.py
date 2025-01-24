from scripting.sys.aws_variables import *
from scripting.sys.sys_functions import *
from scripting.loader.models import site
import argparse
import json
"""
Script to initialize the AWS services for the site.
Run only ones for each site.
"""
sqs_client = session.client('sqs')

sqs_attributes = {
    'FifoQueue': 'true',
    'ContentBasedDeduplication': 'true',
    'DelaySeconds': '60',
    'MaximumMessageSize': '262144',
    'MessageRetentionPeriod': '86400',
    'VisibilityTimeout': '240',
    'ReceiveMessageWaitTimeSeconds': '0',
}

def create_s3_buckets(config_data):
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/")
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/placement/")
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/page/")
    
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/placement/response_data/")
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/placement/parsed_data/")
    
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/page/response_data/")
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site']}/page/parsed_data/")

    return {
        's3_placement_response_data': f"{config_data['site']}/placement/response_data/",
        's3_placement_parsed_data': f"{config_data['site']}/placement/parsed_data/",
        's3_page_response_data': f"{config_data['site']}/page/response_data/",
        's3_page_parsed_data': f"{config_data['site']}/page/parsed_data/",
    }

def create_table_record(config_data):
    site.Site.create(name=config_data['site'], url=config_data['seed_url'])

def create_queue_sqs(queue_name):
    response = SQS_CLIENT.create_queue(
        QueueName= f"{queue_name}.fifo",
        Attributes=sqs_attributes
    )
    return response['QueueUrl']

def reaed_config_file(site_name):
    with open(f"./scripting/site_configurations/{site_name}.json", "r") as file:
        return json.load(file)
    
def put_site_config_ddb(config_data):
    SITE_TABLE.put_item(Item=config_data)

if __name__ == "__main__":
    arg_page = argparse.ArgumentParser(description="Parase arguemtn for init_site script")
    arg_page.add_argument("--site_name")
    args = arg_page.parse_args()
    config_data = reaed_config_file(args.site_name)
    config_data.update(create_s3_buckets(config_data))
    config_data['sqs_crawler'] = create_queue_sqs(f"{args.site_name}_crawler")
    config_data['sqs_parser'] = create_queue_sqs(f"{args.site_name}_parser")
    config_data['sqs_plugin_loader'] = create_queue_sqs(f"{args.site_name}_plugin_loader")
    config_data['sqs_page_loader'] = create_queue_sqs(f"{args.site_name}_loader")
    # create_table_record(config_data)
    put_site_config_ddb(config_data)
