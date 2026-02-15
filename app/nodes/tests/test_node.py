from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader

from app.chains.data_extraction import extraction_chain, Invoice
from app.nodes.store import insert_data

load_dotenv()

def test_insert_data()-> None:
    file_path = "data/Dataset with char-spaced IBAN/invoice_0_charspace_1.pdf"
    loader = PyMuPDFLoader(file_path)
    document = loader.load()
          
    invoice: Invoice = extraction_chain.invoke({
          "page_content": document[0].page_content, 
          "metadata": document[0].metadata,
          "summarize": []
     })
     
    status = insert_data({"invoice": invoice})
    assert status == True