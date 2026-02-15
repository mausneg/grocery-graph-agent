from dotenv import load_dotenv

from app.chains.query_generation import generation_chain
from app.state import SQLState

def generate_query(state: SQLState):
    schema = state["schema"]
    question = state["question"]

    result =  generation_chain.invoke({
        "schema": schema,
        "question": question
    })

    return {"query": result.query}
