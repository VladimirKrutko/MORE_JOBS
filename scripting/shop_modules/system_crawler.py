import requests
from datetime import datetime
from scripting.shop_modules.base_crawler import BaseCrawler

class Crawler(BaseCrawler):
    def __init__(self, http_method='GET'):
        self.http_method = http_method
    
    def fetch(self, url, http_method='GET', headers=None, cookies=None, proxy=None, post_body=None):
        try:
            if http_method.upper() == 'GET':
                response = requests.get(url, headers=headers, cookies=cookies, proxies=proxy)
            elif http_method.upper() == 'POST':
                response = requests.post(url, headers=headers, cookies=cookies, proxies=proxy, data=post_body)
            return response.text, response.status_code, response.headers
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def crawl(self, url, http_method='GET',headers=None ,cookies=None, proxy=None, post_body=None):
        print(f"Start Crawling: {url} at {datetime.now()}")
        html_content, status_code, headers = self.fetch(url, http_method, headers, cookies,proxy, post_body)
        print(f"Done Crawling: {url} at {datetime.now()} {status_code}")
        return html_content, status_code, headers

