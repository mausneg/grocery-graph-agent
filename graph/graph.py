from langgraph.graph import StateGraph, START, END

from graph.conts import LOADER, EXTRACTOR, VALIDATOR
from graph.state import GraphState
from graph.nodes.loader import load_data
from graph.nodes.extractor import extraction
from graph.nodes.validator import validation

def should_continue(state: GraphState):
    if state["is_valid"]:
        return "valid"
    return "not valid"

builder = StateGraph(state_schema=GraphState)
builder.add_node(LOADER, load_data)
builder.add_node(EXTRACTOR, extraction)
builder.add_node(VALIDATOR, validation) 

builder.add_edge(START, LOADER)
builder.add_edge(LOADER, EXTRACTOR)
builder.add_edge(EXTRACTOR, VALIDATOR)
builder.add_conditional_edges(VALIDATOR, should_continue, {
    "valid": END,
    "not valid": EXTRACTOR
})

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
