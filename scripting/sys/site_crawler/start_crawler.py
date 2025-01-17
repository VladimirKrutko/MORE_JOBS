from scripting.sys.process_logger import Logger
from scripting.sys.aws_initialization import *
from scripting.sys.site_data import SiteData
from scripting.sys.sys_functions import *
import importlib
import argparse
import time
import pdb

"""
sqs crawler message format:
{
    "site": "site_name",
    "url": "site_url",
    "mode: "page" or "placement"
}
"""
# data = {"url": "http://example.com/page1","file": 'test', "site": "example.com", "status": "200", "message": "Success"}

def log(site_data, sqs_message, log_message, response=None):
    Logger.log(
        process_name="crawler",
        site=site_data.site_name,
        url=sqs_message['url'],
        status=response['status'] if response else 0,
        message=log_message,
        mode=sqs_message['mode'],
    )

def process_response(site_data, response, message):
    file_path = f"{s3_response_path(site_data, message)}/{message['id']}.html"
    S3_CLIENT.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=response)
    SQS_CLIENT.delete_message(QueueUrl=site_data.sqs_crawler, ReceiptHandle=message['receipt_handle'])
    SQS_CLIENT.send_message(
        QueueUrl=site_data.sqs_parser,
        MessageBody=json.dumps({
            "site": site_data.site_name,
            "url": message['url'],
            "mode": message['mode'],
            "s3_path": file_path,
            }
        )
    )

def s3_response_path(site_data, message):
    return getattr(site_data, f's3_{message["mode"]}_response_data')

def start_crawler(site_data, site_crawler, site_login):
    counter = 0
    login_data = site_login.login()
    while True:
        pdb.set_trace()
        message = listeting_sqs(site_data.sqs_crawler)
        log(site_data, message, "start crawler")
        try:
            time.sleep(site_data.crawler_delay)
            response = site_crawler.crawl(message['url'],login_data['headers'], login_data['cookies'])
            if response['status'] == 200:
                log(site_data, message, "success", response)
            else:
                log(site_data, message, "failed", response)
                continue
            process_response(site_data, response['content'], message)
        except Exception as e:
            response['status'] = 0
            log(site_data, message, str(e), response)
            continue
        if counter % site_data.relogin_interval == 0:
            login_data = site_login.login()
        counter += 1


        
        
def get_site_crawler(site_data):
    module_path = ''
    if site_data.system_crawler is True:
        module_path = "scripting.shop_modules.system_crawler"
    else:
        module_path = f"scripting.shop_modules.{site_data.site_name}.crawler"
    module = importlib.import_module(module_path)
    return getattr(module, 'Crawler')

def get_site_login(site_data):
    module =  importlib.import_module(f"scripting.shop_modules.{site_data.site}.login")
    return getattr(module, 'Login')   

if __name__ == "__main__":
    arg_page = argparse.ArgumentParser(description="Parase arguemtn for init_site script")
    arg_page.add_argument("--site_name")
    args = arg_page.parse_args()
    site_data = SiteData(args.site_name)
    site_crawler = get_site_crawler(site_data)()
    site_login = get_site_login(site_data)()
    start_crawler(site_data, site_crawler, site_login)
