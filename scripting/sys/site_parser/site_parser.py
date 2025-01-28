from scripting.sys.site_data import SiteData
from scripting.sys.sys_functions import *
import importlib
import os
import pdb

class SiteParser:
    def __init__(self, site, mode):
        configure_logging()
        self.mode = mode
        self.site_data = SiteData(site)
        self.is_placement = mode == 'placement'
        self.parser = self.get_parser_classs()
        self.listening_queue = self.site_data.sqs_placement_parser if self.is_placement else self.site_data.sqs_page_parser

    def get_parser_classs(self):
        parser_file = 'placement_parser' if self.is_placement else 'page_parser'
        parser_module = importlib.import_module(f"scripting.shop_modules.{self.site_data.site}.{parser_file}")
        return getattr(parser_module, 'Parser')(self.site_data.site)
    
    def parse(self):
        while True:
            message_data = listeting_sqs(self.listening_queue)
            if message_data['message']['mode'] != self.mode:
                continue
            logging.info(f"Parse s3 file: {message_data['message']['s3_path']}")
            page_content = read_s3_object(message_data['message']['s3_path'])
            try:
                parsed_data = self.parser.parse(page_content, message_data['message']['url'])
            except:
                logging.error(f"Error while parsing page: {message_data['message']['url']}")
                message_data['message']['step'] = 'parsing'
                send_message_to_sqs(SQS_ERORR, str(message_data['message']))
                upate_page_status(message_data['message']['url'], URL_STATUS['error'])
                continue
            parsed_data['site'] = self.site_data.site
            parsed_data['url'] = message_data['message']['url']
            base_path = self.site_data.s3_placement_parsed_data if self.is_placement else self.site_data.s3_page_parsed_data
            file_path = os.path.join(base_path, f"{create_file_name_from_url(message_data['message']['url'])}.json")
            s3_loder_path = put_s3_object(json.dumps(parsed_data), file_path, content_type='application/json')
            sqs_url = self.site_data.sqs_plugin_loader if self.is_placement else self.site_data.sqs_page_loader
            send_message_to_sqs(sqs_url, str({'s3_path': s3_loder_path}))
            delete_message_from_sqs(self.listening_queue, message_data['message_receipt_handle'])
