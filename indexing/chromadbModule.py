import chromadb
from typing import List
from .embeddings import EmbeddingUtility
from langchain_community.vectorstores import Chroma
from langchain_core.documents.base import Document

class ChromadbClient(object):
    def __new__(cls,):
        if not hasattr(cls,'instance'):
            cls.instance = super(ChromadbClient,cls).__new__(cls)
        return cls.instance
            
    def __init__(self):
        self.chroma_client = chromadb.HttpClient(host="localhost",port=8000)
        self.collection_name = None
        self.langchain_chroma = None
        self.embeddings = EmbeddingUtility()
    
    def get_or_create_colletion(self, embedding, collection_name):
        """
        This function will check if collection has data or not
        """
        self.collection_name = collection_name
        
        self.langchain_chroma = Chroma(client=self.chroma_client,collection_name=self.collection_name,embedding_function=embedding.embedding_model)
        print(self.langchain_chroma)
        
        return self.chroma_client.get_or_create_collection(name=self.collection_name)
    
    def get_colletion_items_count(self):
        """
        This function will check if collection has data or not
        """
        return self.chroma_client._count(self.chroma_client.get_collection(name=self.collection_name).id)
        
    def add_data_into_collection(self, embeddings, documents:List[str]):
        """Add new data into db in new or existing collection.

        Args:
            embeddings: Vector values of documents.
            documents: list of strings
            
        Returns:
            This function returns nothing
        """
        
        # Mock Ids and metadata (HAS TO BE IMPLEMENTED AS PER STANDARDS)
        ids = [f"id{i}" for i in range(self.get_colletion_items_count(),self.get_colletion_items_count()+len(documents))]
        metaData = [{"source": "my_source"} for i in range(0,len(documents))]
        

        self.chroma_client.delete_collection(name=self.collection_name)
        self.chroma_client.get_or_create_collection(self.collection_name).add(ids=ids,
                                embeddings=embeddings,documents=documents,metadatas=metaData)
        # self.chroma_client.get_collection(self.collection_name).add(ids=ids,
        #                         embeddings=embeddings,documents=documents,metadatas=metaData)
        
    def query_data(self, query:str):
        """Retrieve data from Database

        Args:
            query: strings
            embedding: Vector values of query string.
            
        Returns:
            the response object from Chroma DB
        """
        
        result = self.langchain_chroma.similarity_search_with_score(query,k=1)
        print("DATA BASE RESULT: \n",[res[0] for res in result])
        return [res[0] for res in result]