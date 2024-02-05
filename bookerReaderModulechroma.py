from langchain.evaluation.qa import QAEvalChain
import config
from indexing.ContenLoaderModule import ContentLoader
from indexing.DocumentTransformerModule import DocumentTransformer
from indexing.QdrantModule import QdrantVectorDB
from indexing.chromadbModule import Database
from chains.QnAChain import QnAChain
from chains.evaluationModule import qa_evaluation_chain
import re

openai_api_key = config.OPENAI_API_KEY
llm_model = config.LLM_MODEL
collection_name = config.COLLECTION_NAME


class BookerReaderModule():
        def check_if_url_contains(self,query):
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

                qVDBObj = QdrantVectorDB(
                    config.DB_CONNECTION_URL, config.DB_CONNECTION_PORT, config.COLLECTION_NAME)
                qdClient = qVDBObj.initializeClient()
                qdbConnection = qVDBObj.connectDB(qdClient)
                docStore = qVDBObj.querySimilaritySearchbyVector(
                    qdbConnection, query)
                print("Here is the response from QDrant:\n", docStore)

            # return docStore

            # invoke Q&A chain
                mychain = QnAChain(type="stuff")
                response = mychain.invokeChain(docStore, query)
                print(response)
                print(response.get('output_text'))
                return response.get('output_text')


        def preProcessDataIndexing(self, fileType, fileURL):
                # Loading the data from PDF file.
                # data = ContentLoader.loadFile(fileType="PDF", fileURL="data/field-guide-to-data-science.pdf")
                data = ContentLoader.loadFile(fileType=fileType, fileURL=fileURL)

                # Using transformer to split
                texts = DocumentTransformer.text_splitter(data)

                # Create Qdrant Collection for Uploading Book ( First time execution only.)
                # docStore = QdrantVectorDB.uploadDataFromScratch(texts)
                docStore = self.uploadDataFromScratch([texts])
                # return docStore
                
        def uploadDataFromScratch(texts):

                currentDB = Database("49ers34-31")
                # embeddings = EmbeddingUtility()
                # # self.chain = QAChain()

                # self.database.get_or_create_colletion()
                # if not self.check_if_data_exist():

                # loaded_document_chunks = self.load_documents()

                # print(f"Total Document length is {len(loaded_document_chunks)}")
                # text_doc_list = [
                #         text.page_content for text in loaded_document_chunks]

                # embeddings = self.create_embeddings(text_doc_list)

                # self.store_data_and_embeddings(embeddings, text_doc_list)
                

# b = BookerReaderModule()
# print(b.check_if_url_contains("Hey! this is me, syed. this is my website https://www.w3schools.com/python/trypython.asp?filename=demo_regex"))