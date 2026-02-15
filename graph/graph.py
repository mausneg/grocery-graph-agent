from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from graph.conts import LOADER, EXTRACTOR, VALIDATOR, STORE
from graph.state import GraphState
from graph.nodes.loader import load_data
from graph.nodes.extractor import extraction
from graph.nodes.validator import validation
from graph.nodes.store import insert_data

load_dotenv()

def should_continue(state: GraphState):
    if state["is_valid"]:
        return "valid"
    return "not valid"

builder = StateGraph(state_schema=GraphState)
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