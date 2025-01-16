from MORE_JOBS.scripting.sys.site_data import SiteData
from MORE_JOBS.scripting.sys.sys_functions import *
import importlib
import argparse


def start_crawler(site_data):
    while True:
        message = listeting_sqs(site_data.sqs_crawler)

        


def get_site_crawler(site_data):
    module_path = ''
    if site_data.system_crawler is True:
        module_path = "MORE_JOBS.scripting.crawler.system_crawler"
    else:
        module_path = f"MORE_JOBS.scripting.crawler.{site_data.site_name}.crawler"
    module = importlib.import_module(module_path)
    return getattr(module, 'Cralwer')


        
    # site_data = SiteData(site_name)
    # print(site_data)

if __name__ == "__main__":
    arg_page = argparse.Argumentpage(description="Parase arguemtn for init_site script")
    arg_page.add_argument("--site_name")
    args = arg_page.parse_args()
    site_data = SiteData(args.site_name)
    site_crawler = get_site_crawler(site_data)()
    
    # site_config = read_yaml(args.site_name)