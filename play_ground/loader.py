import requests
import time

class Loader:
    TIME_POWER = 1000000
    
    def crawler(self, url, data_type):
        crawl_data = requests.get(url).text
        file_name = f"{data_type}_{int(time.time() * Loader.TIME_POWER )}.html"
        with open(f'./temp_data/{file_name}', 'w') as file:
            file.write(crawl_data)
        return file_name