from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import config

"""
    - This class will create embeddings for list of document 
    - or will create query embeddings
"""


class EmbeddingUtility():

    def __init__(self) -> None:
        self.embedding_model = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY)
        print("id(self.embedding_model)",id(self.embedding_model))

    def embed_list_of_documents(self, list: List[str]):
        """This function creates embedding of list of strings NOT DOCUMENT.

        Args:
            list: Supply the list of strings

        Returns:
            list of embedding vectors.
        """

        return self.embedding_model.embed_documents(list)

    def embed_string(self, query: str):
        """ This function creates embedding of a string / query.

        Args:
            query: string 

        Returns:
            embedding vector of query.
        """

        return self.embedding_model.embed_query(query)


# c =EmbeddingUtility()
# print(len(c.embed_list_of_documents(["this is me"])))