import boto3

class Site:
    __TABLE = boto3.resource('dynamodb', region_name='eu-central-1').Table('site-data')

    def __init__(self, site):
        self.__dict__.update(self.load_site_data(site))

    def load_site_data(self, site):
        self.__TABLE.get_item(Key={'site': site})['Item']
