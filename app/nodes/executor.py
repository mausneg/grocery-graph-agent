from dotenv import load_dotenv
import re

from app.database import db
from app.state import SQLState

load_dotenv()

def execution_query(state: SQLState):
    query = state["query"]
    query = re.sub(r'```(?:sql)?\s*|\s*```|;', '', query, flags=re.IGNORECASE).strip()
    
    try:
        result = db.run(query)
        if result:
            return {"result": f"Query executed successfully. Result: {result}"}
        else:
            return {"result": "Query executed successfully, but no results returned."}
    except Exception as e:
        return {"error_message": state.get("error_message", "") + e}
