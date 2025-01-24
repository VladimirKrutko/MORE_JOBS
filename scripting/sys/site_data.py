from scripting.sys.aws_variables import SITE_TABLE
class SiteData:
    def __init__(self, site):
        self.__dict__.update(self.load_site_data(site))

    def load_site_data(self, site):
        return SITE_TABLE.get_item(Key={'site': site})['Item']
