from dotenv import load_dotenv

from graph.graph import graph

load_dotenv()

def main():
    print("Hello from invoice-graph-agent!")
    graph.invoke({"data_path": "data/Dataset with char-spaced IBAN/invoice_16_charspace_17.pdf"})


if __name__ == "__main__":
    main()
