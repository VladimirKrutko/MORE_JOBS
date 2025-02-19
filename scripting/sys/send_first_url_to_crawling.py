from scripting.sys.site_data import SiteData
from scripting.sys.sys_functions import *
import argparse

if __name__ == '__main__':
    print("Start")
    configure_logging()
    arg_page = argparse.ArgumentParser(description="Parase arguemtn for init_site script")
    arg_page.add_argument("--site_name")
    args = arg_page.parse_args()
    site_data = SiteData(args.site_name)
    logging.info("Starting crawler for site: %s start url: %s sqs url: %s", site_data.site, site_data.start_url, site_data.sqs_crawler)
    message = {
        'site': site_data.site,
        'url': site_data.start_url,
        'mode': 'placement',
        }
    send_message_to_sqs(site_data.sqs_crawler, str(message) )
