from scripting.shop_modules.base_parser import *
from .base_methods import BaseMethods
from json_repair import repair_json
import sys

class Parser(BaseParser, BaseMethods):
    JSON_PATTERN = r"window\['kansas-offerview'\]\s*=\s*(\{.*?\});"
    WORKING_TIME = 8
    WORKING_DAYS = 20
    JSON_PATHS = {
        'company_name': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'displayEmployerName'),
        'company_description': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'),
        'offer_title': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'jobTitle'),
        'position_level': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'positionLevels'),
        'technologies': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'textSections'),
        'requirements': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'),
        'responsibilities': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'sections'),
        'language': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'jobOfferLanguage', 'isoCode'),
        'salary': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'typesOfContracts'),
        'work_type': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'employment', 'workModes'),
        'location': ('props', 'pageProps', 'dehydratedState', 'queries', 0, 'state', 'data', 'attributes', 'workplaces'),
    }

    def __init__(self, parsed_site):
        super().__init__(parsed_site)

    def parse(self, page_content, url):
        sys.setrecursionlimit(15000)
        result = self.RESULT_TEMPLATE.copy()
        self.initialize_variables(page_content, url)
        self.parse_offer_data(result)
        return self.process_result(result)

    def parse_offer_data(self, result):
        result['url'] = self.url
        result['company_name'] = self.get_json_value(self.page_json, self.JSON_PATHS['company_name'])
        result['company_description'] = self.parse_company_description()
        result['offer_title'] = self.get_json_value(self.page_json, self.JSON_PATHS['offer_title'])
        result['position_level'] = self.get_json_value(self.page_json, self.JSON_PATHS['position_level'])
        result['technology_list'] = self.parse_technology_list()
        result['offer_description'] = self.parse_offer_description()
        result['requirements'] = self.parse_rr_section('requirements')
        result['responsibilities'] = self.parse_rr_section('responsibilities')
        result['language'] = self.get_json_value(self.page_json, self.JSON_PATHS['language'])
        result['salary'] = self.parse_salary()
        result['work_type'] = self.parse_work_type()
        result['city'] = list(self.parse_location('city'))
        result['country'] = list(self.parse_location('country'))
        return result

    def parse_work_type(self):
        work_type = self.get_json_value(self.page_json, self.JSON_PATHS['work_type'])
        try:
            return [wt['code'] for wt in work_type] if work_type else None
        except:
            return [wt['code'] for wt in work_type['applying']['workModes']] if work_type else None

    def parse_location(self, location_type):
        location_data = self.get_json_value(self.page_json, self.JSON_PATHS['location'])
        location_result = set()
        for location in location_data:
            if location_type == 'city':
                location_result.add(location['inlandLocation']['location']['name'])
            elif location_type == 'country':
                location_result.add(location['country']['name'])
            else:
                location_result.add(None)
        return location_result

    def parse_offer_description(self):
        desc_section = self.find_section(self.get_json_value(self.page_json, self.JSON_PATHS['company_description']), 'about-project')
        return self.squish(" ".join(desc_section['model']['paragraphs'])) if desc_section else None
    
    def parse_salary(self):
        salary_data = self.get_json_value(self.page_json, self.JSON_PATHS['salary'])

        if salary_data[0]['salary'] is None:
            return '-'

        process_salary = lambda salary: {
            'salary_amount': f"{salary['from']}-{salary['to']}",
            'employment_type': salary['name'],
            'currency': salary['salary']['currency']['code'],
            'time_unit': salary['timeUnit']['longForm']['name'],
        }
        return list(map(process_salary, salary_data)) if salary_data else None

    # def salary_amount(self, salary):
    #     if salary is None:
    #         return '-'
    #     return {
    #         'salary_amount': f"{salary['from']}-{salary['to']}",
    #     }
    #         # f"{salary['from'] * self.WORKING_TIME * self.WORKING_DAYS}-{salary['to'] * self.WORKING_TIME * self.WORKING_DAYS}"
    #         # if salary['timeUnit']['longForm']['name'] != 'monthly'
    #         # else f"{salary['from']}-{salary['to']}"

    def parse_rr_section(self, section_name):
        base_section = self.get_json_value(self.page_json, self.JSON_PATHS['company_description'])
        description_section = self.find_section(base_section, section_name)
        join_bullets = lambda section: "@@@@".join(section['model']['bullets'])

        if description_section.get('subSections'):
            return "@@@@".join(
                [join_bullets(sub_section) for sub_section in description_section['subSections']]
            ) if description_section else None
        return join_bullets(description_section) if description_section else None
    
    def parse_technology_list(self):
        technology_list = {}
        offer_technologies = self.get_json_value(self.page_json, self.JSON_PATHS['technologies'])
        get_technology = lambda tech: next(
            (t for t in offer_technologies if t['sectionType'] == tech or t['sectionType'] == f"{tech}\""), {}
        )
        required_technologies = get_technology('technologies-expected')
        expected_technologies = get_technology('technologies-optional')
        req_key = [key for key in required_technologies.keys() if 'textElements' in key]
        exp_key = [key for key in expected_technologies.keys() if 'textElements' in key]
        technology_list['required'] = required_technologies.get(req_key[0]) if len(req_key) > 0 else None
        technology_list['optional'] = expected_technologies.get(exp_key[0]) if len(exp_key) > 0 else None
        return technology_list

    def parse_company_description(self):
        base_section = self.get_json_value(self.page_json, self.JSON_PATHS['company_description'])
        description_section = self.find_section(base_section, 'about-us-description')
        return self.squish(" ".join(description_section['model']['paragraphs'])) if description_section else None

    def find_section(self, section_list, section_name):
        return next((section for section in section_list if section['sectionType'] == section_name or section['sectionType'] == f"{section_name}\""), None)

    def extract_json(self):
        json_text = self.doc.find("script", attrs={"id": re.compile(r".*__NEXT_DATA__.*")}).string        
        return json.loads(repair_json(json_text))

    def get_json_value(self, json_obj, json_path):
        for key in json_path:
            try:
                json_obj = json_obj[key]
            except (IndexError, KeyError, TypeError):
                return json_obj
        return json_obj
