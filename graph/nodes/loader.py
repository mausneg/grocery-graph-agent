
from langchain_community.document_loaders import PyMuPDFLoader
import os
from dotenv import load_dotenv

from graph.state import GraphState

load_dotenv()

def load_data(state: GraphState):
    print("Loading data...")
    data_path =  state["data_path"]
    loader = PyMuPDFLoader(data_path)
    document = loader.load()
                
    return {"document": document}
    