from scripting.sys.aws_initialization import session
from scripting.sys.process_logger import ProcessLogger
from scripting.sys.site_data import SiteData
import importlib

class SiteParser:
    def __init__(self, site, parser_import_path):
        self.parser_import_path = parser_import_path
        self.site_data = SiteData(site)
        self.parser = self.parser_object()
        self.logger = ProcessLogger('parser')
        
    def parser_object(self):
        parser_module = importlib.import_module(self.parser_import_path)
        return getattr(parser_module, 'Parser')
    
    def parse(self):
        sqs_client = session.client('sqs')
        s3_client = session.client('s3')
        while True:
            response = sqs_client.receive_message(
                QueueUrl=self.parser_queue,
                MaxNumberOfMessages=1,
                VisibilityTimeout=20,
                WaitTimeSeconds=20
            )
            if 'Messages' in response:
                message = response['Messages'][0]
                message_body = message['Body']
                message_receipt_handle = message['ReceiptHandle']
                message_id = message['MessageId']
                message_body = json.loads(message_body)
                url = message_body['url']
                response_result = self.parser().get_response(url)
                if response_result:
                    s3_client.put_object(Bucket=self.s3_bucket, Key=f"{self.site_data.site}/plugin/response_data/{message_id}", Body=json.dumps(response_result))
                    parsed_data = self.parser().parse(response_result, url)
                    s3_client.put_object(Bucket=self.s3_bucket, Key=f"{self.site_data.site}/plugin/parsed_data/{message_id}", Body=json.dumps(parsed_data))
                    sqs_client.send_message(
                        QueueUrl=self.loader_queue,
                        MessageBody=json.dumps({
                            'url': url,
                            'parsed_data': parsed_data
                        })
                    )
                sqs_client.delete_message(
                    QueueUrl=self.parser_queue,
                    ReceiptHandle=message_receipt_handle
                )
            else:
                self.logger.info('No message in queue')
        
        
        # return self.parser().parse(response_result, url)