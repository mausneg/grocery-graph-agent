from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from app.state import SQLState
from app.conts import SCHEMA, GENERATOR_QUERY, VALIDATOR_QUERY, EXECUTOR, REPAIR, EXECUTOR, GENERATOR_ANSWER
from app.nodes.schema import get_schema
from app.nodes.generator_query import generate_query
from app.nodes.validator_query import validate_query
from app.nodes.executor import execution_query
from app.nodes.repair import repair_query
from app.nodes.generator_answer import generate_answer

load_dotenv()

def is_dangerous(state: SQLState):
    if state["is_dangerous"]:
        return "dangerous"
    return "safe"

def is_error(state: SQLState):
    error_message = state["error_message"]
    if error_message:
        return "error"
    return "success"

builder = StateGraph(state_schema=SQLState)
builder.add_node(SCHEMA, get_schema)
builder.add_node(GENERATOR_QUERY, generate_query)
builder.add_node(VALIDATOR_QUERY, validate_query)
builder.add_node(EXECUTOR, execution_query)
builder.add_node(REPAIR, repair_query)
builder.add_node(GENERATOR_ANSWER, generate_answer)

builder.add_edge(START, SCHEMA)
builder.add_edge(SCHEMA, GENERATOR_QUERY)
builder.add_edge(GENERATOR_QUERY, VALIDATOR_QUERY)
builder.add_conditional_edges(VALIDATOR_QUERY, is_dangerous, {
    "dangerous": GENERATOR_ANSWER   ,
    "safe": EXECUTOR
})
builder.add_conditional_edges(EXECUTOR, is_error, {
    "error": REPAIR,
    "success": GENERATOR_ANSWER
})
builder.add_edge(REPAIR, EXECUTOR)
builder.add_edge(GENERATOR_ANSWER, END)

graph_query = builder.compile()
graph_query.get_graph().draw_mermaid_png(output_file_path="graph-query.png")