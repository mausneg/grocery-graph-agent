from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DATABASE")

db = SQLDatabase.from_uri(f"mysql+pymysql://{USER}:{PASSWORD}@127.0.0.1:{PORT}/{DB_NAME}?charset=utf8mb4")