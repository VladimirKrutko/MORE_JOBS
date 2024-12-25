
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

def create_s3_buckets(config_data):
    s3_client = session.client('s3')
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site_name']}/")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site_name']}/plugin")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site_name']}/parser")
    
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site_name']}/plugin/response_data")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site_name']}/plugin/parsed_data")
    
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site_name']}/parser/response_data")
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f"{config_data['site_name']}/parser/parsed_data")

def create_table_record(config_data):
    site.Site.create(name=config_data['site_name'], url=config_data['seed_url'])

def create_queue_parser(config_data):
    pass

def create_queue_plugin(config_data):
    pass

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

    
    
    
    
