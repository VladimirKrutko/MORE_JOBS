from scripting.sys.process_logger import Logger
from scripting.sys.site_data import SiteData
from scripting.sys.sys_functions import *
import importlib
import pdb

class SiteParser:
    def __init__(self, site, mode):
        configure_logging()
        self.mode = mode
        self.site_data = SiteData(site)
        self.is_placement = mode == 'placement'
        self.parser = self.get_parser_classs()
        self.listening_queue = self.site_data.sqs_parser

    def get_parser_classs(self):
        parser_file = 'placement_parser' if self.is_placement else 'page_parser'
        parser_module = importlib.import_module(f"scripting.shop_modules.{self.site_data.site}.{parser_file}")
        return getattr(parser_module, 'Parser')(self.site_data.site)
    
    def parse(self):
        while True:
            pdb.set_trace()
            message_data = listeting_sqs(self.site_data.sqs_parser)
            if message_data['message']['mode'] != self.mode:
                continue
            logging.info(f"Parse s3 file: {message_data['message']['s3_path']}")
            page_content = read_s3_object(message_data['message']['s3_path'])
            parsed_data = self.parser.parse(page_content, message_data['message']['url'])
            parsed_data['site'] = self.site_data.site
            base_path = self.site_data.s3_placement_parsed_data if self.is_placement else self.site_data.s3_page_parsed_data
            s3_loder_path = put_s3_object(parsed_data, message_data['message_id'], base_path)
            send_message_to_sqs(self.site_data.sqs_placement_loader if self.is_placement else self.site_data.sqs_page_loader, str({'s3_path': s3_loder_path}))
            delete_message_from_sqs(self.site_data.sqs_parser, message_data['message_receipt_handle'])
