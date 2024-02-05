from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import config

class QnAChain:
    def __init__(self, type="stuff"):
        self.llm = ChatOpenAI(temperature=0, model=config.LLM_MODEL, openai_api_key=config.OPENAI_API_KEY)
        self.currentChainInAction = load_qa_chain(self.llm, chain_type=type, verbose=True)

    def invokeChain(self, documentStore, query):
        return self.currentChainInAction.invoke({'input_documents': documentStore, 'question': query})