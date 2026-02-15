from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class QueryFixedGeneration(BaseModel):
    fixed_query: str = Field(description="The fixed SQL query, only SELECT statements are allowed")

prompt = PromptTemplate.from_template(
    """
    The following SQL query failed:
    schema: {schema}
    Query: {query}
    Error: {error_message}
    Original Question: {question}

    Analyze the error and provide a corrected SQL query that:
    1. Fixed the specific error mentioned
    2. Still answer the original question
    3. Used only valid table and column names from the schema
    4. Follows SQLite syntax rules

    Return only the corrected SQL query, nothing else.
    """
)
llm = ChatOllama(model="qwen2.5:3b", temperature=0).with_structured_output(QueryFixedGeneration)

query_fix_chain = prompt | llm