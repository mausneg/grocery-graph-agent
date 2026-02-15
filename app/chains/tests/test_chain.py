from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv
from pprint import pprint

from app.chains.data_extraction import extraction_chain, Invoice
from app.chains.data_validation import validation_chain, DataValidation
from app.chains.query_generation import query_chain, QueryGenerated
from app.chains.query_fix import query_fix_chain, QueryFixedGeneration
from app.chains.anwser_generation import anwser_chain, AnswerGeneration
from app.database import db

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

def test_query_generation()-> None:
     schema = db.get_table_info()
     question = "What is the total net worth in 2020?"
     
     result: QueryGenerated = query_chain.invoke({
          "schema": schema,
          "question": question
     })

     print(result.query)
     assert result.query.strip().upper().startswith("SELECT")

def test_query_fix_generation()-> None:
     schema = db.get_table_info()
     question = "What is the total net worth in 2020?"
     wrong_query = "SELECT SUM(net_worth) AS total_net_worth FROM invoices WHERE strftime('%Y', extracted_at) = '2020' GROUP BY strftime('%Y', extracted_at) LIMIT 10"
     error_message = "FUNCTION grocery_agent_db.strftime does not exist"

     result: QueryFixedGeneration = query_fix_chain.invoke({
          "question": question,
          "error_message": error_message,
          "query": wrong_query
     })

     print(result.fixed_query)
     assert result.fixed_query.strip().upper().startswith("SELECT")

def test_answer_generation()-> None:
     question = "What is the total net worth in 2020?"
     query = "SELECT SUM(net_worth) AS total_net_worth FROM invoices WHERE YEAR(issue_date) = 2020 GROUP BY YEAR(issue_date) LIMIT 10"

     query_result = db.run(query)
     print(query_result)

     result: AnswerGeneration = anwser_chain.invoke({
          "question": question,
          "query_result": query_result
     })

     print(result.answer)