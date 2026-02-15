from typing import TypedDict
from langchain_core.documents import Document

from app.chains.data_extraction import Invoice
from app.chains.data_validation import Summarize
class InvoiceState(TypedDict):
    data_path: str
    invoice: Invoice
    document: Document
    is_valid: bool
    summarize: Summarize
    success: bool

class SQLState(TypedDict):
    question: str
    schema: str
    query: str
    error_message: str
    is_dangerous: bool
    result: str
    answer: str