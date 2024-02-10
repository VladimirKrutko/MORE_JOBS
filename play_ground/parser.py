import json
import time
from bs4 import BeautifulSoup

class Parser:
    TIME_POWER = 1000000
    
    def __init__(self, file_path, base_file_name):
        self.doc = self.create_doc(file_path)
        self.base_file_name = base_file_name
        
    def create_doc(self, file_path):
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
        return soup
    
    def parse_json(self):
        return json.loads(self.doc.find('script', id='__NEXT_DATA__').string)
    
    def save_data(self, data):
        with open(f'./page_data/{self.base_file_name}.json', 'w') as file:
            json.dump(data, file)
            
    def create_todo(self, data): 
       urls = [offer['offers'][0]['offerAbsoluteUri'] for offer in data]
       with open(f'./todos/{int( time.time() * Parser.TIME_POWER )}_todo.txt', 'w') as file:
           for url in urls:
               file.write(url + '\n')
                
    def parse(self):
        json_data = self.parse_json()
        offers_data = json_data['props']['pageProps']['data']['jobOffers']['groupedOffers']
        self.save_data(offers_data)
        self.create_todo(offers_data)
        
        
        
        
        