from langchain_openai import ChatOpenAI
from langchain.evaluation.qa import QAEvalChain
from langchain.evaluation.qa.generate_chain import QAGenerateChain
import config
class qa_evaluation_chain:
    
    @staticmethod
    def evaluate(texts):
        example_question_generation_chain = QAGenerateChain.from_llm(ChatOpenAI(model=config.LLM_MODEL))

        example_questions = example_question_generation_chain.apply_and_parse(
            [{"doc": item.page_content} for item in texts[:1]])

        print("data: \n", texts[0].page_content,
            "\nExample Question: \n", example_questions)


        # generated_qa_evaluation_chain = QAEvalChain.from_llm(ChatOpenAI(temperature=0, model=config.LLM_MODEL))
        # print(generated_qa_evaluation_chain.evaluate(example_questions[0]["query"], list(response)))
        # return generated_qa_evaluation_chain
