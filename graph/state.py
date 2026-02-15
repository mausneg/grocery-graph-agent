from typing import TypedDict
from langchain_core.documents import Document

from graph.chains.data_extraction import Invoice
from graph.chains.data_validation import Summarize
class GraphState(TypedDict):
    data_path: str
    invoice: Invoice
    document: Document
    is_valid: bool
    summarize: Summarize
    sucess: bool