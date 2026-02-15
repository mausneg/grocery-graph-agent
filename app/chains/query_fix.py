from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class QueryFixedGeneration(BaseModel):
    fixed_query: str = Field(description="The fixed MySQL query, only SELECT statements are allowed")

prompt = PromptTemplate.from_template(
    """
    The following MySQL query failed:
    Original Query: {query}
    Error message: {error_message}
    Original Question: {question}

    Analyze the error and provide a corrected MySQL query that:
    1. Fixed the specific error mentioned
    2. Still answer the original question
    3. Used only valid table and column names from the schema
    4. Follows MySQL syntax and best practices
    """
)
llm = ChatOllama(model="qwen3:4b").with_structured_output(QueryFixedGeneration)

query_fix_chain = prompt | llm