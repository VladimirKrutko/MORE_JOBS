from airflow_module.dags_code.data_processing import DataProcessing
from scripting.sys.static_meta import StaticMeta
from scripting.loader.chroma_db import ChromaDB
from scripting.loader.models.offer import Offer

chroma_db = ChromaDB()

class LLMModelInterface(metaclass=StaticMeta):
    GET_OFFER_PARAMETER_PROMPTS = """
    Extract the next from user text to better user preference in job searching: requirements, responsibilities, technologies, company, salary.
    This text will used to request in the chroma db. 
    From this text (%s). Do not added additional information only requested data. With out comments only requirements, responsibilities, technologies, salary.
    """
    # And return result in the next format: 'requirements': '...'\n 'responsibilities': '...'\n'technologies': '...'\n'company': '...'\b'salary': '...'.
    # If the text is not contains any of the above, fill the missing fields with empty string. Please return only text in the format mentioned above.

    def get_offer_parameters(user_text: str):
        llm_prompt = LLMModelInterface.GET_OFFER_PARAMETER_PROMPTS % user_text
        return DataProcessing.llama_local_request(llm_prompt).lower()

    def augmented_prompt(context: str, query_text: str):
        return f"Context: User made request to the chroma db with the following text: {query_text}. \
        The chroma db returned the following documents: {context}. Please generate a response to the user."
    
    def get_response_according_chromadb(user_text: str):
        chroma_doc = LLMModelInterface.get_offer_parameters(user_text)
        chroma_db_response =  chroma_db.query_base_collection(chroma_doc)
        context = " ".join(chroma_db_response['documents'][0]) if chroma_db_response['documents'] else "No relevant documents found."
        prompt = LLMModelInterface.augmented_prompt(context, user_text)
        return {
            'llm_text': DataProcessing.llama_local_request(prompt),
            'documents': chroma_db_response['documents'][0],
            'ids': chroma_db_response['ids']
            }
    