import requests
import time

class Loader:
    TIME_POWER = 1000000
    
    def crawler(self, url, data_type):
        crawl_data = requests.get(url).text
        with open(f'./temp_data/{data_type}_{int(time.time() * Loader.TIME_POWER )}' +  + '.txt', 'w') as file:
            file.write(crawl_data)