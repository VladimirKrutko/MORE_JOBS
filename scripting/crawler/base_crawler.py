from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    @abstractmethod
    def to_recrwale(self, responce_result):
        """
        Conditition for check responce reslut 
        """
        pass
    
    @abstractmethod
    def crawl(self, task):
        """
        Base method that should be realize in all creawlers
        """
        pass