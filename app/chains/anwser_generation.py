from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class AnswerGeneration(BaseModel):
    answer: str = Field(description="The generated answer to the user's question based on the query result and the question.")

prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant that generates an answer to the user's question based on the query result and the question.

    Question: {question}
    Query Result: {query_result}
    """
)
llm = ChatOllama(model="qwen2.5:7b", temperature=0).with_structured_output(AnswerGeneration)

anwser_chain = prompt | llm
