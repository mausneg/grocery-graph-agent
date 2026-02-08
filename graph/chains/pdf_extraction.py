from typing import Optional
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class User(BaseModel):
    name: str = Field(description="User name")
    tax_id: str = Field(description="Tax identification number")
    iban: str = Field(description="IBAN")
    address: str = Field(description="User address")

class InvoiceItem(BaseModel):
    line_no: int = Field(description="Line number")
    description: str = Field(description="Item description")
    quantity: int = Field(description="Quantity")
    net_price: float = Field(description="Net price")
    net_worth: float = Field(description="Net worth")
    vat: float = Field(description="VAT")
    gross_worth: float = Field(description="Gross worth")

class Invoice(BaseModel):
    invoice_number: str = Field(description="Unique invoice number")
    issue_date: datetime = Field(description="Invoice issue date format YYYY-MM-DD")
    seller: User = Field(description="Seller user")
    client: User = Field(description="Client user")
    currency: str = Field(description="Currency")
    net_worth: float = Field(description="Net worth")
    vat_total: float = Field(description="VAT total")
    gross_worth: float = Field(description="Gross worth")
    pdf_path: str = Field(description="PDF file path")
    extracted_at: datetime = Field(description="Extraction datetime")
    invoice_items: list[InvoiceItem] = Field(description="List of invoice items")

prompt = PromptTemplate.from_template(
    """Extract the invoice data from the following PDF page content.

    Page Content:
    {page_content}

    Metadata:
    {metadata}
    
    Current datetime:
    {extracted_at}
    
        
    Return the data in JSON format matching the Invoice schema.
    """
).partial(extracted_at=datetime.now().isoformat())
llm = ChatOllama(model="qwen2.5:7b", temperature=0).with_structured_output(Invoice)
# llm = ChatOpenAI(temperature=0).with_structured_output(Invoice)

extraction_chain = prompt | llm