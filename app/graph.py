from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from app.conts import LOADER, EXTRACTOR, VALIDATOR, STORE
from app.state import InvoiceState
from app.nodes.loader import load_data
from app.nodes.extractor import extraction
from app.nodes.validator_data import validation
from app.nodes.store import insert_data

load_dotenv()

def should_continue(state: InvoiceState):
    if state["is_valid"]:
        return "valid"
    return "not valid"

builder = StateGraph(state_schema=InvoiceState)
builder.add_node(LOADER, load_data)
builder.add_node(EXTRACTOR, extraction)
builder.add_node(VALIDATOR, validation) 
builder.add_node(STORE, insert_data)

builder.add_edge(START, LOADER)
builder.add_edge(LOADER, EXTRACTOR)
builder.add_edge(EXTRACTOR, VALIDATOR)
builder.add_conditional_edges(VALIDATOR, should_continue, {
    "valid": STORE,
    "not valid": EXTRACTOR
})
builder.add_edge(STORE, END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")