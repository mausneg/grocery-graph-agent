from dotenv import load_dotenv

from app.state import InvoiceState
from app.chains.data_validation import validation_chain

def validation(state: InvoiceState):
    print("Validating invoice data...")
    invoice = state["invoice"]
    validation_result = validation_chain.invoke(invoice)
    
    return {"is_valid": validation_result.is_valid, "summarize": validation_result.summarize}
