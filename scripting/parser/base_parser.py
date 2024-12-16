from abc import ABC, abstractmethod

class BaseParser(ABC):
    RESULT_TEMPLATE = {
        'url': None,
        'site': 'pracuj.pl',
        'company_name': None,
        'company_url': None,
        'company_description': None,
        'offer_title': None,
        'position_level': None,
        'technology_list': None,
        'offer_description': None,
        'requirements': None,
        'responsibilities': None,
        'language': None,
        'city': None,
        'salary': None,
        'work_type': None,
    }
    
    def __init__(self, parsed_site):
        self.parsed_site = parsed_site
    
    @abstractmethod
    def initalize_variables():
        pass
    
    @abstractmethod
    def parse(self, response_result):
        return dict