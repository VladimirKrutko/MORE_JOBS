from .base_methods import *
from scripting.parser.base_parser import BaseParser

class Parser(BaseParser, BaseMethods):
    
    def parse(self, response_result, url):
        self.initialize_variables(response_result, url)
        return self.create_result()
    
    def create_result(self):
        return {
            'offer_urls': self.parse_offer_urls(), 
            'next_page': self.pagination(),
            }

    def parse_offer_urls(self):
        links = self.doc.find_all("a", attrs={"data-test": re.compile(r"^link-offer$")})
        return [link['href'] for link in links]
    
    def pagination(self):
        page_number = self.get_page_number()
        if page_number == self.last_page():
            return None
        
        return f"{self.url}?pn=2" if page_number == 1 else re.sub(r"(\d+)", str(page_number+1), self.url)
        
    def get_page_number(self):
        page_number = re.search(r"(\d+)", self.url)
        return int(page_number.group(0)) if page_number else 1
     
    def last_page(self):
        pages = self.doc.find_all("button", {"data-test": lambda value: value and "bottom-pagination-button-page" in value})
        return max([int(p.text.strip()) for p in pages])
