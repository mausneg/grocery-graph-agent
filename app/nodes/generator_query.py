from dotenv import load_dotenv

from app.chains.query_generation import query_chain
from app.state import SQLState

load_dotenv()

def generate_query(state: SQLState):
    print("Generating SQL query based on the question and schema...")
    schema = state["schema"]
    question = state["question"]

    result =  query_chain.invoke({
        "schema": schema,
        "question": question
    })

    return {"query": result.query, "error_message": ""}
