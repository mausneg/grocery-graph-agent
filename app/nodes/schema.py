from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

from app.state import SQLState
from app.database import db

def get_schema(state: SQLState):
    schema = db.get_table_info()
    return {"schema": schema}
