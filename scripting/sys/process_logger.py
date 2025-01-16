from scripting.loader.models import crawl_log, loader_log, parser_log
"""
This is a simple logger class that logs the data based on the process name.
"""
class Logger:

    @staticmethod
    def log(self, **kwargs):
        if kwargs['process_name'] == 'crawl':
            crawl_log.CrawlLog.create(**kwargs)
        elif kwargs['process_name'] == 'loader':
            loader_log.LoaderLog.create(**kwargs)
        elif kwargs['process_name'] == 'parser':
            parser_log.ParserLog.create(**kwargs)
        else:
            raise ValueError('Invalid process name')