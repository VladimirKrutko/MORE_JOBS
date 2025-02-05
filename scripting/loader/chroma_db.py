from scripting.sys.sys_functions import (LLAMA_API, 
                                         LLM_MODEL, 
                                         CHROMA_DB_CLIENT, 
                                         CHROMA_COLLECTION_NAME)
from chromadb import EmbeddingFunction, OllamaEmbeddings

class ChromaDBEmbeddingFunction(EmbeddingFunction):
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input: list):
        return self.langchain_embeddings.embed_documents(input)

embedding = ChromaDBEmbeddingFunction(
    OllamaEmbeddings(
        model=LLM_MODEL,
        base_url=LLAMA_API
        )
        )

chroma_collection = CHROMA_DB_CLIENT.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    embedding_function=embedding
    )

class ChromaDB:

    def __init__(self, num_results: int = 10):
        self.collection = chroma_collection
        self.num_results = num_results
    
    def query_chroma_db(self, document: str):
        """
        Query the chroma db for the given document:
        Args:
            document (str): The document to query the chroma db with.
        Returns:
        dict: {document: ..., metadata: ...}
        """
        result = self.collection.query(
            document=document,
            num_results=self.num_results
        )
        return {
            'document': result['documents'],
            'metadata': result['metadata']
        }
    
