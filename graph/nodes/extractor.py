from dotenv import load_dotenv

from graph.chains.data_extraction import extraction_chain
from graph.state import GraphState

load_dotenv()

def extraction(state: GraphState):
    print("Extracting data from document...")
    docs = state["document"]
    summarize = state.get("summarize", [])
    results = extraction_chain.invoke({
        "page_content": docs[0].page_content,
        "metadata": docs[0].metadata,
        "summarize": summarize
    })
    
    return {"invoice": results}
    