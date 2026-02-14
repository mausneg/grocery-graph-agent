from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv
from pprint import pprint

from graph.chains.data_extraction import extraction_chain, Invoice
from graph.chains.data_validation import validation_chain, DataValidation

load_dotenv()

def test_extraction_result()-> None:
     file_path = "data/Dataset with char-spaced IBAN/invoice_0_charspace_1.pdf"
     loader = PyMuPDFLoader(file_path)
     document = loader.load()
          
     invoice: Invoice = extraction_chain.invoke({
          "page_content": document[0].page_content, 
          "metadata": document[0].metadata,
          "summarize": []
     })
     pprint(invoice)
     
def test_validation_answer_true()-> None:
     file_path = "data/Dataset with char-spaced IBAN/invoice_0_charspace_1.pdf"
     loader = PyMuPDFLoader(file_path)
     document = loader.load()
          
     invoice: Invoice = extraction_chain.invoke({
          "page_content": document[0].page_content, 
          "metadata": document[0].metadata,
          "summarize": []
     })
     data_validation: DataValidation = validation_chain.invoke(invoice)
     
     assert data_validation.is_valid == True
     
def test_validation_answer_false()-> None:
     file_path = "data/Dataset with char-spaced IBAN/invoice_0_charspace_1.pdf"
     loader = PyMuPDFLoader(file_path)
     document = loader.load()
          
     invoice: Invoice = extraction_chain.invoke({
          "page_content": document[0].page_content, 
          "metadata": document[0].metadata,
          "summarize": []
     })
     invoice.invoice_items[0].quantity = 999
     
     data_validation: DataValidation = validation_chain.invoke(invoice)
     
     assert data_validation.is_valid == False