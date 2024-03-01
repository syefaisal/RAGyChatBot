from langchain.evaluation.qa import QAEvalChain
import config
from indexing.ContenLoaderModule import ContentLoader
from indexing.DocumentTransformerModule import DocumentTransformer
from indexing.chromadbModule import ChromadbClient
from indexing.embeddings import EmbeddingUtility
from chains.QnAChain import QnAChain
from chains.evaluationModule import qa_evaluation_chain
from typing import List
import re

openai_api_key = config.OPENAI_API_KEY
llm_model = config.LLM_MODEL
collection_name = config.COLLECTION_NAME


class BookerReaderModule():
        def __init__(self):
                """
                First it will initiate the DB and check if collection and data doesnot exist then it will:
                - Create collections
                - Load documents 
                - Create embedding
                - Then store data and embeddings in collections
                """
                self.database = ChromadbClient()
                self.embeddings = EmbeddingUtility()
                # self.chain = QAChain()


        def check_if_url_contains(self,query):
                """
                This is a Utility function to check if a message contains URL.
                
                Returns:
                - Returns String value as  "True" if URL exists in the query.
                - Returns String value as  "False" if URL does not exist.

                Example:
                        bookReader.check_if_url_contains(query)
                """
                regex = re.compile(
                r'^https?://|'  # http:// or https://
                # domain...
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                
                for item in query.split(' '):
                        contains_url = re.match(regex,item)
                        if contains_url:
                                return contains_url.string.lower()
                return None

        def process_user_query(self, query):

                # qVDBObj = QdrantVectorDB(
                #     config.DB_CONNECTION_URL, config.DB_CONNECTION_PORT, config.COLLECTION_NAME)
                # qdClient = qVDBObj.initializeClient()
                # qdbConnection = qVDBObj.connectDB(qdClient)
                # docStore = qVDBObj.querySimilaritySearchbyVector(
                #     qdbConnection, query)
                self.database.get_or_create_colletion(self.embeddings, "49ers34-31")
                print("count ->",self.database.get_colletion_items_count())
                docStore = self.database.query_data(query)
                print("Here is the response from DB:\n", docStore)

                # invoke Q&A chain
                mychain = QnAChain(type="stuff")
                response = mychain.invokeChain(docStore, query)
                # print(response)
                print(response.get('output_text'))
                return response.get('output_text')


        def preProcessDataIndexing(self, fileType, fileURL):
                # Loading the data from PDF file.
                data = ContentLoader.loadFile(fileType=fileType, fileURL=fileURL)
                
                # Using transformer to split
                texts = DocumentTransformer.text_splitter(data)

                # Create Qdrant Collection for Uploading Book ( First time execution only.)
                # docStore = QdrantVectorDB.uploadDataFromScratch(texts)
                docStore = self.uploadDataFromScratch(texts)
                return docStore
                
        def uploadDataFromScratch(self,texts):

                self.database.get_or_create_colletion(self.embeddings, "49ers34-31")
                print("current Items in collection",self.database.get_colletion_items_count())
                if not self.check_if_data_exist():
                        print("current Items in collection",self.database.get_colletion_items_count())
                        text_doc_list = [text.page_content for text in texts]
                        # print(text_doc_list)
                        embeddings = self.create_embeddings(text_doc_list)
                        # print("embeddings->", embeddings)
                        self.store_data_and_embeddings(embeddings, text_doc_list)
                        print("count ->",self.database.get_colletion_items_count())
                        # print(int("49ers34-31"))
                        


        def check_if_data_exist(self):
                """
                This functions checks the count of items in the collection 

                return: if 0 then False otherwise True
                """
                result = False if self.database.get_colletion_items_count() == 0 else True
                print("IF DB EXIST OR NOT: ", result)
                # return result        
                return False

        def create_embeddings(self, text_doc_list: List[str]):
                """
                This function create the embeddings against the list provided

                args: text_doc_list: List[str]

                return: embeddings of list of documents:str
                """
                return self.embeddings.embed_list_of_documents(text_doc_list)
        

        def store_data_and_embeddings(self, embeddings, text_document_list):
                """
                This functions stores embeddings and list of strings in collections.

                args: embeddings:List[float]
                text_document_list: List[str]

                """
                self.database.add_data_into_collection(embeddings, text_document_list)