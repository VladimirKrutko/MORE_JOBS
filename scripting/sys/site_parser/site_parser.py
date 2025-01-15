from scripting.sys.process_logger import ProcessLogger
from scripting.sys.aws_initialization import session
from scripting.sys.site_data import SiteData
from scripting.sys.sys_variables import *
import importlib
import json

class SiteParser:
    SQS_CLIENT = session.client('sqs')
    S3_CLIENT = session.client('s3')

    def __init__(self, site, parser_import_path, mode):
        self.parser_import_path = parser_import_path
        self.site_data = SiteData(site)
        self.parser = self.parser_object(site)
        self.logger = ProcessLogger('parser')
        self.is_placement = mode == 'placement'
        self.listening_queue = self.site_data.placement_parser_queue if self.is_placement else self.site_data.page_parser_queue

    def parser_object(self, site):
        parser_module = importlib.import_module(self.parser_import_path)
        return getattr(parser_module, 'Parser')(site)
    
    def parse(self):
        while True:
            message_data = self.sqs_message_data()
            page_content = self.get_s3_content(message_data['message']['s3_path'])
            parsed_data = self.parser.parse(page_content, message_data['message']['url'])
            parsed_data['site'] = self.site_data.site
            s3_loder_path = self.put_s3_object(parsed_data, message_data['message']['message_id'])
            self.SQS_CLIENT.receive_message(
                QueueUrl= self.site_data.sqs_placement_loader if self.is_placement else self.site_data.sqs_page_loader,
                MessageBody=json.dumps({'s3_path': s3_loder_path}),
                )
            self.SQS_CLIENT.delete_message(
                QueueUrl=self.listening_queue,
                ReceiptHandle=message_data['message_receipt_handle']
            )

    def put_s3_object(self, data, file_name):
        base_path = self.site_data.s3_placement_parsed_data if self.is_placement else self.site_data.s3_page_parsed_data
        s3_path = f"{base_path}/{file_name}.json"
        self.S3_CLIENT.put_object(Bucket=BACKET_NAME, Key=s3_path, Body=json.dumps(data))
        return s3_path
        
    def get_page_content(self, s3_path):
        response = self.S3_CLIENT.get_object(Bucket=BACKET_NAME, Key=s3_path)
        return response['Body'].read().decode('utf-8')

    def sqs_message_data(self):
        while True:
            response = self.SQS_CLIENT.receive_message(
                QueueUrl= self.listening_queue,
                MaxNumberOfMessages=1,
                VisibilityTimeout=30,
                WaitTimeSeconds=20
            )
            if 'Messages' in response:
                message = response['Messages'][0]
                return {
                    'message': json.loads(message['Body']),
                    'message_receipt_handle': message['ReceiptHandle'],
                    'message_id': message['MessageId']
                }
