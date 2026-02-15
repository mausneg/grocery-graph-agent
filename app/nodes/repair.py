from dotenv import load_dotenv

from app.state import SQLState
from app.chains.query_fix import query_fix_chain

load_dotenv()

def repair_query(state: SQLState):
    print("Repairing query...")
    query = state["query"]
    error_message = state["error_message"]
    question = state["question"]

    result = query_fix_chain.invoke({
        "query": query,
        "error_message": error_message,
        "question": question
    })

    return {"query": result.fixed_query}