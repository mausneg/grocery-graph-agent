from dotenv import load_dotenv

from app.state import SQLState
from app.chains.query_fix import query_fix_chain

load_dotenv()

def repair_query(state: SQLState):
    query = state["query"]
    error_message = state["error_message"]
    schame = state["schema"]
    question = state["question"]

    result = query_fix_chain.invoke({
        "query": query,
        "error_message": error_message,
        "schema": schame,
        "question": question
    })

    return {"query": result.fixed_query}