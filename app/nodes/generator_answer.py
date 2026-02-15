from dotenv import load_dotenv

from app.state import SQLState
from app.chains.anwser_generation import anwser_chain

load_dotenv()

def generate_answer(state: SQLState):
    print("Generating answer...")
    question = state["question"]
    result = state["result"]
    
    answer = anwser_chain.invoke({
        "question": question,
        "query_result": result
    })
    return {"answer": answer}