import json
from bs4 import BeautifulSoup

class BaseParser:
    def __init__(self, resonce_result, response_code, response_headers, url):
        self.page_content = resonce_result
        self.response_code = response_code
        self.response_headers = response_headers
        self.url = url

    def parse(self):
        pass