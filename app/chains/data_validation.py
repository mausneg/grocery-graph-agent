from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from pprint import pprint

from app.chains.data_extraction import Invoice

load_dotenv()

class Summarize(BaseModel):
    error: Optional[str] = Field(description="A report of error found during validation")
    pay_attention: Optional[str] = Field(description="Points that user should pay attention to fix")

class DataValidation(BaseModel):
    is_valid: bool = Field(description="Indicates if the extracted invoice data is valid")
    summarize: Summarize = Field(description="A list of summaries highlighting validation results")
    
def invoice_check(invoice: Invoice):
    reports = []
    total_net_worth = 0.0
    total_gross_worth = 0.0

    for item in invoice.invoice_items:
        qty = int(item.quantity)
        price = float(item.net_price)
        vat = float(item.vat)

        net_worth = round(qty * price, 2)
        gross_worth = round(net_worth * (1 + vat / 100.0), 2)
        
        reports.append(
            f"""
            Reported net worth for invoice item line {item.line_no}.
            Calculated: {net_worth}
            Extracted: {item.net_price}
            Difference: {abs(net_worth - float(item.net_worth))}
            """
        )
        
        reports.append(
            f"""
            Reported gross worth for invoice item line {item.line_no}.
            Calculated: {gross_worth}
            Extracted: {item.gross_worth}
            Difference: {abs(gross_worth - float(item.gross_worth))}
            """
            )
            
        total_net_worth += net_worth
        total_gross_worth += gross_worth

    total_net_worth = round(total_net_worth, 2)
    total_gross_worth = round(total_gross_worth, 2)

    reports.append(
        f"""
        Reported total net worth for invoice.
        Calculated: {total_net_worth}
        Extracted: {invoice.net_worth}
        Difference: {abs(total_net_worth - float(invoice.net_worth))}
        """
    )

    reports.append(
        f"""
        Reported total gross worth for invoice.
        Calculated: {total_gross_worth}
        Extracted: {invoice.gross_worth}
        Difference: {abs(total_gross_worth - float(invoice.gross_worth))}
        """
    )
    return reports

prompt = PromptTemplate.from_template(
    """
    Given list of reports on the extracted invoice data, determine if the data is valid.
    Give is valid or not with 'True' or 'False' answer.
    If the difference values are within acceptable limits (e.g., less or equal to 0.01), consider the data valid.
    And you should provide a summary of the validation results so the user can pay attention to fixing them.
    
    Invoice:
    {invoice}
    
    Reports:
    {reports}
    """
)
llm = ChatOllama(model="qwen3:4b", temperature=0).with_structured_output(DataValidation)

validation_chain = (
    {
        "reports": RunnableLambda(invoice_check),
        "invoice": RunnablePassthrough()
    }
    | prompt
    | llm
)