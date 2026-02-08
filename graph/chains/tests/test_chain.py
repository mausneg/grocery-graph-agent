from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv
from pprint import pprint

from graph.chains.pdf_extraction import extraction_chain

load_dotenv()

def test_extraction_result()-> None:
    docs = []
    for i in range(3):
         file_path = f"data/Dataset with char-spaced IBAN/invoice_{i}_charspace_{i+1}.pdf"
         loader = PyMuPDFLoader(file_path)
         docs.extend(loader.load())
         
    result = extraction_chain.batch([{"page_content": doc.page_content, "metadata": doc.metadata} for doc in docs])
    pprint(result)