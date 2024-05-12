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
        li_tag = self.doc.find_all('li', attrs={"data-test": lambda x: x and 'item-technologies' in x})
        technologies = [ p.find_all('p')[0] if len(p.find_all('p'))>0 else None for p in li_tag]
        technologies = [ p.text for p in technologies if p is not None]
        # technologies = [ p.text for p in self.doc.select("//li[ contains(@data-test, 'item-technologies')]/p")]
        print(f"tech {technologies}")
        url = self.doc.find('meta', {'property': 'og:url'})['content']
        print(f"url {len(url)}")
        data =  { key: page_json[key] if key in page_json.keys() else None for key in PageParser.PARSED_FILEDS}
        data['technologies'] = ",".join(technologies) if len(technologies) > 0 else None
        data['url'] = url
        return data
        
