from dotenv import load_dotenv

from app.chains.data_extraction import extraction_chain
from app.state import InvoiceState

load_dotenv()

def extraction(state: InvoiceState):
    print("Extracting data from document...")
    docs = state["document"]
    summarize = state.get("summarize", [])
    results = extraction_chain.invoke({
        "page_content": docs[0].page_content,
        "metadata": docs[0].metadata,
        "summarize": summarize
    })
    
    return {"invoice": results}
    