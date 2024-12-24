from scripting.parser.base_parser import *

class BaseMethods:
    def initialize_variables(self, page_content, url):
        self.url = url
        self.doc = BeautifulSoup(page_content, 'html.parser')
        self.page_json = self.extract_json()
        
    def extract_json(self):
        return {}
    
    @staticmethod
    def squish(text):
        return re.sub(r'\s+', ' ', text).strip()