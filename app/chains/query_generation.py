from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class QueryGenerated(BaseModel):
    query: str = Field(description="The generated SQL query")
    
llm = ChatOllama(base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),model="qwen3:4b").with_structured_output(QueryGenerated)
prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant that generates MySQL queries based on a given database schema and a question.
    Rules:
    - Include only exiting columns and tables
    - Add appropriate WHERE, GROUP BY, ORDER BY clauses as needed
    - Limit results to 10 rows unless specified otherwisem

    Database Schema:
    {schema}

    Question:
    {question}
    """
)

query_chain = prompt | llm
