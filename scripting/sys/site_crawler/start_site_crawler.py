from scripting.sys.process_logger import Logger
from scripting.sys.site_data import SiteData
from scripting.sys.aws_variables import *
from scripting.sys.sys_functions import *
import importlib
import argparse
import signal
import time
import os

"""
sqs crawler message format:
{
    "site": "site_name",
    "url": "site_url",
    "mode: "page" or "placement"
}
"""

signal.signal(signal.SIGINT, signal_handler)

def log(site_data, sqs_message, log_message, response=None):
    Logger.log(
        process_name="crawl",
        site=site_data.site,
        url=sqs_message['message']['url'],
        status=response['status'] if response else 0,
        message=log_message,
        mode=sqs_message['message']['mode'],
    )

def process_response(site_data, response, message):
    file_path = os.path.join(s3_response_path(site_data, message), f"{message['message_id']}.html")
    put_s3_object(response, file_path)
    delete_message_from_sqs(site_data.sqs_crawler, message['message_receipt_handle'])
    message = {
            "site": site_data.site,
            "url": message['message']['url'],
            "mode": message['message']['mode'],
            "s3_path": file_path,
            }
    send_message_to_sqs(site_data.sqs_parser, str(message))

def s3_response_path(site_data, message):
    return getattr(site_data, f's3_{message["message"]["mode"]}_response_data')

def start_crawler(site_data, site_crawler, site_login):
    counter = 0
    login_data = site_login.login()
    while True:
        message = listeting_sqs(site_data.sqs_crawler)
        log(site_data, message, "start crawler")
        try:
            logging.info(f"Get url: {message['message']['url']} Sleep for {site_data.crawler_delay} seconds")
            time.sleep(int(site_data.crawler_delay))
            response = site_crawler.crawl(url=message['message']['url'], headers=login_data['headers'], cookies=login_data['cookies'])
            if response['status'] == 200:
                logging.info(f"Success response from {message['message']['url']}")
                log(site_data, message, "success", response)
            else:
                logging.error(f"Failed response from {message['message']['url']}")
                log(site_data, message, "failed", response)
                continue
            process_response(site_data, response['content'], message)
        except Exception as e:
            response['status'] = 0
            logging.error(f"Error on process page {message['message']['url']} {str(e)}")
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
        module_path = f"scripting.shop_modules.{site_data.site}.crawler"
    module = importlib.import_module(module_path)
    return getattr(module, 'Crawler')

def get_site_login(site_data):
    module =  importlib.import_module(f"scripting.shop_modules.{site_data.site}.login")
    return getattr(module, 'Login')   

if __name__ == "__main__":
    configure_logging()
    arg_page = argparse.ArgumentParser(description="Parase arguemtn for init_site script")
    arg_page.add_argument("--site_name")
    args = arg_page.parse_args()
    site_data = SiteData(args.site_name)
    site_crawler = get_site_crawler(site_data)()
    site_login = get_site_login(site_data)()
    start_crawler(site_data, site_crawler, site_login)
