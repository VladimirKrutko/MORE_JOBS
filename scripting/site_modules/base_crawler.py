from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    _instances = {'GET': None, 'POST': None}

    def __new__(cls, http_method='GET', *args, **kwargs):
        http_method = http_method.upper()
        if http_method not in ['GET', 'POST']:
            raise ValueError("Only 'GET' and 'POST' methods are supported")
        
        if cls._instances[http_method] is None:
            instance = super(BaseCrawler, cls).__new__(cls)
            cls._instances[http_method] = instance
        return cls._instances[http_method]
    
    @abstractmethod
    def crawl(self, task):
        """
        Base method that should be realize in all crawlers
        """
        pass
    