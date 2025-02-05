from airflow_module.dags_code.data_processing import DataProcessing
from scripting.sys.static_meta import StaticMeta
from scripting.loader.chroma_db import ChromaDB

chroma_db = ChromaDB()

class LLMModelInterface(metaclass=StaticMeta):
    GET_OFFER_PARAMETER_PROMPTS = """
    Extract the next from user text to better user preference in job searching: requirements, responsibilities, technologies, company, salary. 
    From this text (%s). And return result in the next format: 'requirements': '...'\n 'responsibilities': '...'\n'technologies': '...'\n'company': '...'\b'salary': '...'.
    If the text is not contains any of the above, fill the missing fields with empty string. Please return only text in the format mentioned above.
    """

    def get_offer_parameters(user_text: str):
        llm_prompt = LLMModelInterface.GET_OFFER_PARAMETER_PROMPTS % user_text
        return DataProcessing.llama_request(llm_prompt)

    def query_chroma_db(user_text: str):
        query_document = LLMModelInterface.get_offer_parameters(user_text)
        return chroma_db.query_chroma_db(query_document)

    def augmented_prompt(context: str, query_text: str):
        return f"Context: {context}\n\nQuestion: {query_text}\nAnswer:"
    
    def get_response_according_chromadb(user_text: str):
        chroma_db_response = LLMModelInterface.query_chroma_db(user_text)
        context = " ".join(chroma_db_response['documents']) if chroma_db_response['documents'] else "No relevant documents found."
        prompt = LLMModelInterface.augmented_prompt(context, user_text)
        return DataProcessing.llama_local_request(prompt)
