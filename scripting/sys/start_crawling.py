from scripting.sys.sys_functions import SQS_CLIENT, MESSAGE_GROUP
from scripting.sys.site_data import SiteData
import argparse

if __name__ == '__main__':
    arg_page = argparse.ArgumentParser(description="Parase arguemtn for init_site script")
    arg_page.add_argument("--site_name")
    args = arg_page.parse_args()
    site_data = SiteData(args.site_name)
    print(site_data.sqs_crawler)
    SQS_CLIENT.send_message(
        QueueUrl=site_data.sqs_crawler,
        MessageBody=str(
            {
            'site': site_data.site,
            'url': site_data.start_url,
            'mode': 'placement',
            }
            ),
        MessageGroupId=MESSAGE_GROUP,
        )
    
