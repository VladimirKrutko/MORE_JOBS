import time
import requests
from LoginScript import LoginScript

class CustomLoader:
    TIME_POWER = 1000000
    ACCES_DENIED = 'Access denied | www.pracuj.pl used Cloudflare to restrict access'
    
    headers = {
        'authority': 'www.pracuj.pl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

    def load(url, cookies):
        response = requests.get(
        url,
        cookies=cookies,
        headers=CustomLoader.headers,)
        return response.text
    
    def crawl(url, data_type, cookies):
        crawl_data = CustomLoader.load(url, cookies)
        if CustomLoader.ACCES_DENIED in crawl_data:
            return False
        else:
            file_name = f"{data_type}_{int(time.time() * CustomLoader.TIME_POWER )}.html"
            with open(f'./temp_data/{file_name}', 'w') as file:
                file.write(crawl_data)
            return file_name

