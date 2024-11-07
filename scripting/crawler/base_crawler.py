from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    @abstractmethod
    def crawl(self, task):
        """
        Base method that should be realize in all creawlers
        """
        pass