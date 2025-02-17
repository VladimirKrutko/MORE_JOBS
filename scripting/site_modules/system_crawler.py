from scripting.site_modules.base_crawler import BaseCrawler
from datetime import datetime
import requests


class Crawler(BaseCrawler):
    DEFAULT_HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language':'pl,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    def __init__(self, http_method='GET'):
        self.http_method = http_method
    
    def fetch(self, url, http_method='GET', headers=None, cookies=None, proxy=None, post_body=None):
        try:
            if http_method.upper() == 'GET':
                response = requests.get(url, headers=headers if headers else self.DEFAULT_HEADERS, cookies=cookies, proxies=proxy)
            elif http_method.upper() == 'POST':
                response = requests.post(url, headers=headers, cookies=cookies, proxies=proxy, data=post_body)
            return response.text, response.status_code, response.headers
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def crawl(self, url, http_method='GET',headers=None ,cookies=None, proxy=None, post_body=None):
        print(f"Start Crawling: {url} at {datetime.now()}")
        html_content, status_code, headers = self.fetch(url, http_method, headers, cookies, proxy, post_body)
        print(f"Done Crawling: {url} at {datetime.now()} {status_code}")
        return {
            'content': html_content,
            'status': status_code,
            'headers': headers
        }

