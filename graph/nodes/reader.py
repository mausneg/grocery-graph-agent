
from langchain_community.document_loaders import PyMuPDFLoader
import os
from dotenv import load_dotenv

from graph.state import GraphState

load_dotenv()

BASE_PATH = "data"

def read_data(state: GraphState):
    docs = []
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(".pdf"):   
                file_path = os.path.join(root, file)
                loader = PyMuPDFLoader(file_path)
                docs.extend(loader.load())
                
    print(len(docs))
    
if __name__ == "__main__":
    read_data({})