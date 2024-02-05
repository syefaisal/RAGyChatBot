from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
import config
class QdrantVectorDB:
    def __init__(self, dbURL, dbPort, dbCollection):
        self.dbURL = config.DB_CONNECTION_URL
        self.dbPort = config.DB_CONNECTION_PORT
        self.collectionName = config.COLLECTION_NAME
        self.embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)


    def initializeClient(self):
        return QdrantClient(self.dbURL, port=self.dbPort)

    def connectDB(self, qdClient):
        return Qdrant(qdClient, embeddings=self.embeddings, collection_name=self.collectionName)
        
    
    def querySimilaritySearchbyVector(self, qDBConnection, query):
        #Following are options WE MUST EXPLORE TO LEARN DIFFERENT WAYS OF SEARCHING VECTORS.
        # simple Similarity search 
        # Similarity search with score
        # Similarity search by vector
        # Maximum marginal relevance search (MMR)
        # Qdrant as a Retriever
        # 
        documentStore = qDBConnection.similarity_search_by_vector(embedding=self.embeddings.embed_query(query))
        # documentStore = qDBConnection.similarity_search_with_score(query)
        # documentStore = qDBConnection.max_marginal_relevance_search(query, k=2, fetch_k=10)
        print("Here is the response from QDrant:\n", documentStore)
        return documentStore
    
    # TODO: Following code is a temporary solution to start VectorDB for start up. Correct solution is to use recreate collection function from Qdrant.
    @staticmethod
    def uploadDataFromScratch(self, qDBConnection, query):
        documentStore = qDBConnection.similarity_search_by_vector(embedding=self.embeddings.embed_query(query))
        print("Here is the response from QDrant:\n", documentStore)
        return documentStore