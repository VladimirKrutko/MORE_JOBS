from scripting.sys.sys_functions import (LLAMA_API, 
                                         LLM_MODEL, 
                                         CHROMA_DB_CLIENT, 
                                         CHROMA_COLLECTION_NAME,
                                         CHROMA_COLLECTION_BASE_NAME)
from langchain_ollama import OllamaEmbeddings
from chromadb import EmbeddingFunction

class ChromaDBEmbeddingFunction(EmbeddingFunction):
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input: list):
        return self.langchain_embeddings.embed_documents(input)

embedding = ChromaDBEmbeddingFunction(
    OllamaEmbeddings(
        model= LLM_MODEL,
        base_url=LLAMA_API
        )
        )

chroma_collection = CHROMA_DB_CLIENT.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    embedding_function=embedding
    )

class ChromaDB:
    def __init__(self, n_results: int = 10):
        self.collection = chroma_collection
        self.n_results = n_results
        self.base_collection = CHROMA_DB_CLIENT.get_or_create_collection(name=CHROMA_COLLECTION_BASE_NAME)
    
    def query_chroma_db(self, document: str):
        """
        Query the chroma db for the given document:
        Args:
            document (str): The document to query the chroma db with.
        Returns:
        dict: {documents: ..., metadatas: ...}
        """
        result = self.collection.query(
            query_texts=document,
            n_results=self.n_results
        )
        return {
            'documents': result['documents'][0],
            'metadatas': result['metadatas']
        }
    
    def query_base_collection(self, document: str):
        """
        Query the base collection for the given document:
        Args:
            document (str): The document to query the base collection with.
        Returns:
        dict: {documents: ..., metadatas: ...}
        """
        result = self.base_collection.query(
            query_texts=document,
            n_results=self.n_results
        )
        return result