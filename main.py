from dotenv import load_dotenv

from app.graph_data import graph_data
from app.graph_query import graph_query


load_dotenv()

def main():
    print("Hello from invoice-graph-agent!")
    # graph_data.invoke({"data_path": "data/Dataset with char-spaced IBAN/invoice_16_charspace_17.pdf"})


if __name__ == "__main__":
    main()
