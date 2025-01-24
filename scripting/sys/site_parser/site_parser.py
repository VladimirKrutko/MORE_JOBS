from scripting.sys.process_logger import Logger
from scripting.sys.site_data import SiteData
from scripting.sys.sys_functions import *
import importlib
import pdb

class SiteParser:
    def __init__(self, site, mode):
        configure_logging()
        self.site_data = SiteData(site)
        self.is_placement = mode == 'placement'
        self.parser = self.get_parser_classs()
        self.listening_queue = self.site_data.placement_parser_queue if self.is_placement else self.site_data.page_parser_queue

    def get_parser_classs(self):
        parser_file = 'placement_parser' if self.is_placement else 'page_parser'
        parser_module = importlib.import_module(f"scripting.site_modules.{self.site_data.site}.{parser_file}")
        return getattr(parser_module, 'Parser')(self.site_data.site)
    
    def parse(self):
        while True:
            pdb.set_trace()
            message_data = listeting_sqs(self.get_queu_url())
            # listeting_sqs(self.get_queu_url())
            logging.info(f"Parse s3 file: {message_data['message']['s3_path']}")
            page_content = read_s3_object(message_data['message']['s3_path'])
            Logger.log()
            # self.get_s3_content(message_data['message']['s3_path'])
            parsed_data = self.parser.parse(page_content, message_data['message']['url'])
            parsed_data['site'] = self.site_data.site
            base_path = self.site_data.s3_placement_parsed_data if self.is_placement else self.site_data.s3_page_parsed_data
            s3_loder_path = put_s3_object(parsed_data, message_data['message']['message_id'], base_path)
            # s3_loder_path = self.put_s3_object(parsed_data, message_data['message']['message_id'])
            send_message_to_sqs(self.site_data.sqs_placement_loader if self.is_placement else self.site_data.sqs_page_loader, str({'s3_path': s3_loder_path}))
            # send_message_to_sqs(self.site_data.sqs_page_loader, str({'s3_path': s3_loder_path}))
            # send_message_to_sqs(self.site_data.sqs_placement_loader if self.is_placement else self.site_data.sqs_page_loader, json.dumps({'s3_path': s3_loder_path}))
            # SQS_CLIENT.receive_message(
            #     QueueUrl= self.site_data.sqs_placement_loader if self.is_placement else self.site_data.sqs_page_loader,
            #     MessageBody=json.dumps({'s3_path': s3_loder_path}),
            #     )
            delete_message_from_sqs(self.get_queu_url(), message_data['message_receipt_handle'])
            # SQS_CLIENT.delete_message(
            #     QueueUrl=self.listening_queue,
            #     ReceiptHandle=message_data['message_receipt_handle']
            # )

    # def put_s3_object(self, data, file_name):
    #     s3_path = f"{base_path}/{file_name}.json"
    #     S3_CLIENT.put_object(Bucket=BACKET_NAME, Key=s3_path, Body=json.dumps(data))
    #     return s3_path
        
    def get_page_content(self, s3_path):
        response = S3_CLIENT.get_object(Bucket=BACKET_NAME, Key=s3_path)
        return response['Body'].read().decode('utf-8')

    def get_queu_url(self):
        return self.site_data.sqs_placement_parser if self.is_placement else self.site_data.sqs_page_parser

    # def listeting_sqs(self, site):
    #     while True:
    #         response = SQS_CLIENT.receive_message(
    #             QueueUrl= self.listening_queue,
    #             MaxNumberOfMessages=1,
    #             VisibilityTimeout=30,
    #             WaitTimeSeconds=20
    #         )
    #         if 'Messages' in response:
    #             message = response['Messages'][0]
    #             return {
    #                 'message': json.loads(message['Body']),
    #                 'message_receipt_handle': message['ReceiptHandle'],
    #                 'message_id': message['MessageId']
    #             }
