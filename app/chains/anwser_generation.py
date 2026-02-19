from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os


load_dotenv()

class AnswerGeneration(BaseModel):
    answer: str = Field(description="The generated answer to the user's question based on the query result and the question.")

prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant that generates an answer to the non-technical user's question based on the query result and the question
    If the query result contains a dangerous message or warning, give answer  with a short polite apology and a reason for non-technical users.

    Question: {question}
    Query Result: {query_result}
    """
)
llm = ChatOllama(base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),model="qwen2.5:7b").with_structured_output(AnswerGeneration)

anwser_chain = prompt | llm
