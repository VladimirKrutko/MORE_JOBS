import importlib
from MORE_JOBS.scripting.sys.site_data import SiteData

class SiteParser:
    def __init__(self, site, parser_queu, s3_bucket, loader_queue, parser_import_path):
        self.parser_queue = parser_queu
        self.s3_bucket = s3_bucket
        self.loader_queue = loader_queue
        self.parser_import_path = parser_import_path
        self.site_data = SiteData(site)
        self.parser = self.parser_object()

    def parser_object(self):
        parser_module = importlib.import_module(self.parser_import_path)
        return getattr(parser_module, 'Parser')
    
    def parse(self):
        pass
        # return self.parser().parse(response_result, url)