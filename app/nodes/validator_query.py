from dotenv import load_dotenv
import re

from app.state import SQLState

def validate_query(state: SQLState):
    query = state["query"]
    dangerous_keywords = ["drop", "delete", "update", "insert", "alter", "create", "truncate", "grant", "revoke"]
    
    query = re.sub(r"```(?:sql)?\s*|\s*```", "", query, flags=re.IGNORECASE).strip()
    if any(keyword in query.lower() for keyword in dangerous_keywords):
        return {"error_message": "The query contains potentially dangerous operations. Only SELECT statements are allowed."}
    if not query.lower().startswith("select"):
        return {"error_message": "Only SELECT statements are allowed."}
    return {"error_message": ""}