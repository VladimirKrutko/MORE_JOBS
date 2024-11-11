import json
from abc import ABC
from bs4 import BeautifulSoup

class BaseParser(ABC):
    def __init__(self, parsed_site):
        self.parsed_site = parsed_site
        self.parse_result = {}
    async def parse(self, response_result):
        return self.parse_result
    