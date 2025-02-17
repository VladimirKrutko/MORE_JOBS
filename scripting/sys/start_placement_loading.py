from scripting.sys.site_data import SiteData
from scripting.sys.sys_functions import *
from scripting.sys.aws_variables import *
import signal
import json

signal.signal(signal.SIGINT, signal_handler)

def sqs_message(url, site_data, mode):
    message = {
        'site': site_data.site,
        'url': url,
        'mode': mode,
        }
    return str(message)

def loader():
    while True:
        message = listeting_sqs(PLACEMENT_LOADER_SQS)
        logging.info(f"Load placement: {message['message']['s3_path']}")
        placement_data = json.loads(read_s3_object(message['message']['s3_path']))
        site_data = SiteData(placement_data['site'])
        logging.info(f"Send next placement url to crawl: {placement_data['next_page']}")
        send_message_to_sqs(site_data.sqs_crawler, sqs_message(placement_data['next_page'], site_data, 'placement'))
        logging.info(f"Send page urls to crawler")
        for url in placement_data['offer_urls']:
            send_message_to_sqs(site_data.sqs_crawler, sqs_message(url, site_data, 'page'))
        logging.info(f"Delete message from sqs: {message['message_receipt_handle']}")
        delete_message_from_sqs(PLACEMENT_LOADER_SQS, message['message_receipt_handle'])

if __name__ == '__main__':
    configure_logging()
    loader()
    