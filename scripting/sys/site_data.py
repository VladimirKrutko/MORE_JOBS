from scripting.sys.aws_initialization import SITE_TABLE
class SiteData:
    def __init__(self, site):
        self.__dict__.update(self.load_site_data(site))

    def load_site_data(self, site):
        SITE_TABLE.get_item(Key={'site': site})['Item']
