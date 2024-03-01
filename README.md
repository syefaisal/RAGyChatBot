# LangChainCookBook
Work related to Langchain and OpenAI

# please create an environment file with the following content


OPENAI_API_KEY_LOCAL=<YOUR Open AI Key.>

LLM_MODEL = gpt-3.5-turbo-0301

QDRANT_COLLECTION_NAME = fg2ds
QDRANT_URL = http://localhost
QDRANT_PORT = 6333
DOC_TYPE = pdf


QDRANT__LOG_LEVEL=INFO
QDRANT__SERVICE__HTTP_PORT=6333
QDRANT__SERVICE__ENABLE_TLS=1
QDRANT__TLS__CERT=./tls/cert.pem
QDRANT__TLS__CERT_TTL=0000



# command to start the project:

streamlit run bookReaderUI.py

User Guide:
- This is a RAG application that is implemented as a ChatBot.
- This RAG application uses streamlit as User Interface for Chat Bot interface.
- User copy pastes an article that is written after 2022. Since That is the last year until ChatGPT is trained with internet datasets.
- Everytime Chat Bot recieves a URL as input then the following steps are exectued: 
    - The RAG converts HTML to Text using HTML2Text library.
    - Creat Chunks using DocumentTransformer RecursiveCharacterTextSplitter with chunk_size=1000, chunk_overlap=0
    - Create Embeddings using ChatGPT. 
    - Use ChromaDB to save Chunks as vectors to ChromaDB
    - ChromaDB has 3 parts.
        - ChromaDB docker container as a server.
        - ChromaDB server has no User Interface.
        - ChromaDB python module.
- After last step for every query that does not have a URL. the RAG will use web URL data as a context.
- So for testing purpose i pick up latest news article URL and paste in the ChatBot. 
- Then ask questions accordingly. 

        