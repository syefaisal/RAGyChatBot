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
