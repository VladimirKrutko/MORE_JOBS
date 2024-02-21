import json
import pdb
from bs4 import BeautifulSoup

class PageParser:
    PARSED_FILEDS = ['employmentType','title', 'industry', 'baseSalary', 'description', 'jobBenefits','responsibilities', 'experienceRequirements']
    
    def __init__(self, file_path) -> None:
        self.doc = self.create_doc(file_path)
        
    def create_doc(self, file_path):
        with open(file_path, 'r', encoding="utf-8" ) as file:
            soup = BeautifulSoup(file, 'html.parser')
        return soup
    
    def parse_json(self):
        page_json = json.loads(self.doc.find('script', type='application/ld+json').string)
        return { key: page_json[key] if key in page_json.keys() else None for key in PageParser.PARSED_FILEDS}
        
        
