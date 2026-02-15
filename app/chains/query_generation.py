from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class GenerationOutput(BaseModel):
    query: str = Field(description="The generated SQL query, only SELECT statements are allowed")
    
llm = ChatOllama(model="qwen2.5:3b", temperature=0).with_structured_output(GenerationOutput)
prompt = PromptTemplate.from_template(
    """
    Based on this databse schema:
    {schema}

    Generate a SQL query to answer this question: {question}

    Rules:
    - Use only SELECT statements
    - Include only exiting columns and tables
    - Add appropriate WHERE, GROUP BY, ORDER BY clauses as needed
    - Limit results to 10 rows unless specified otherwisem
    - Use proper SQL syntax for SQLite

    Return only the SQL query, nothing else. 
    """
)

generation_chain = prompt | llm
