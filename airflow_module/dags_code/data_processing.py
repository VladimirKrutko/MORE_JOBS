from scripting.sys.sys_functions import SQS_CLIENT, OLLAMA_HOST, configure_logging, logging, LLM_MODEL
from langchain_ollama import OllamaLLM
from scripting.loader.models.offer_data import OfferData
from scripting.sys.aws_variables import SQS_LOADER
from scripting.sys.static_meta import StaticMeta
from scripting.loader.db_setup import Session

import requests
import json

configure_logging()

class DataProcessing(metaclass=StaticMeta):
    DATA_TO_TRANSLATE_QUERY = """
    select od.id, od.requirements, od.responsibilities
    from offer_data as od
    where od.original_language <> 'en' and od.translated_data = '{}';
    """
    DATA_TO_TRANSLATE_QUERY ="""
    select od.id, od.requirements, od.responsibilities
    from offer_data as od
    where od.original_language <> 'en' 
    and od.translated_data = '{}'
    and od.id in :offer_data_ids;
    """
    LLM = OllamaLLM(model=LLM_MODEL)

    def get_sqs_loader_message():
        response = SQS_CLIENT.receive_message(
            QueueUrl=SQS_LOADER,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,
            AttributeNames=['All'],
            MessageAttributeNames=['All']
        )
        return [message for message in response['Messages']] if 'Messages' in response else []
    
    def get_offer_data_to_translate():
        session = Session()
        offer_data = session.execute(DataProcessing.DATA_TO_TRANSLATE_QUERY).all()
        logging.info(f"Offer data to translate: {len(offer_data)}")
        session.close()
        return offer_data

    def get_offer_data(offer_data_ids: list = []):
        session = Session()
        offer_data = session.query(OfferData).\
                    filter(OfferData.id.in_(offer_data_ids) if offer_data_ids else offer_data_ids != -1 , OfferData.original_language != 'en').\
                    with_entities(OfferData.id, OfferData.original_language, OfferData.requirements, OfferData.responsibilities).\
                    all()
        session.close()
        return offer_data
    
    def translate_data(translated_text):
        return DataProcessing.TRANSLATOR.translate(translated_text)
        
    def llama_translate_template(translated_data, language='polish'):
        return f"just translate text from {language} to english (return only translated text): {translated_data}"
    
    def llama_request(prompt_text):
        payload = {
            "model": "llama3.1",
            "prompt": prompt_text,
        }
        response = requests.post(OLLAMA_HOST, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        list_dict_words = []
        if response.status_code == 200:
            list_dict_words = []
            for each_word in response.text.split("\n"):
                try:
                    data = json.loads(each_word) 
                except:
                    pass
                list_dict_words.append(data)
        return "".join([word['response'] for word in list_dict_words if type(word) == type({})])
    
    def translate_offer_data(session):
        offer_data = DataProcessing.get_offer_data_to_translate()
        logging.info(f"Offer data to translate: {len(offer_data)}")
        translated_data = []
        for od in offer_data:
            session = Session()
            prompt_req_text = DataProcessing.llama_translate_template(od.requirements)
            prompt_resp_text = DataProcessing.llama_translate_template(od.responsibilities)
            translated_data = {
                'requirements': DataProcessing.llama_request(prompt_req_text).lower(),
                'responsibilities': DataProcessing.llama_request(prompt_resp_text).lower()
            }
            OfferData.update(session, od.id, translated_data=translated_data)
            session.commit()
            logging.info(f"Offer data with id {od.id} translated")
            session.close()

    def llama_local_request(prompt_text):
        return DataProcessing.LLM.invoke(prompt_text)
    # DataProcessing.llama_request(prompt_text)
    
