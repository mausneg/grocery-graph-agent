from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
from sqlalchemy import text
from uuid import uuid4

from app.state import InvoiceState
from app.database import db

load_dotenv()

def insert_data(state: InvoiceState):
    print("Inserting data into database...")
    invoice = state["invoice"]

    try:
        tables = db.get_usable_table_names()
        print(tables)
        print(len(tables))
    except Exception as e:
        print(e)

    client = invoice.client
    seller = invoice.seller
    items = invoice.invoice_items
    invoice_id = str(uuid4())
    client_id = str(uuid4())
    seller_id = str(uuid4())

    user_stmt = text(
        """
        INSERT INTO users (id, name, tax_id, iban, address, created_at)
        VALUES
            (:c_id, :c_name, :c_tax_id, :c_iban, :c_address, NOW()),
            (:s_id, :s_name, :s_tax_id, :s_iban, :s_address, NOW())
        """
    )

    items_stmt = text(
        """
        INSERT INTO invoice_detail (id, description, gross_worth, line_no, net_price, net_worth, quantity, vat, invoice_id)
        VALUES
            (:id, :description, :gross_worth, :line_no, :net_price, :net_worth, :quantity, :vat, :invoice_id)
        """
    )
    invoice_stmt = text(
        """
        INSERT INTO invoices (id, invoice_number, issue_date, seller_id, client_id, currency, net_worth, vat_total, gross_worth, pdf_path, extracted_at, created_at)
        VALUES
            (:id, :invoice_number, :issue_date, :seller_id, :client_id, :currency, :net_worth, :vat_total, :gross_worth, :pdf_path, :extracted_at, NOW())
        """
    )

    try:
        with db._engine.begin() as conn:
            user_params = {
                "c_name": client.name,
                "c_tax_id": client.tax_id,
                "c_iban": client.iban,
                "c_address": client.address,
                "s_name": seller.name,
                "s_tax_id": seller.tax_id,
                "s_iban": seller.iban,
                "s_address": seller.address,
                "c_id": client_id,
                "s_id": seller_id
            }
            conn.execute(user_stmt, user_params)

            invoice_params = {
                "id": invoice_id,
                "invoice_number": invoice.invoice_number,
                "issue_date": invoice.issue_date,
                "seller_id": seller_id,
                "client_id": client_id,
                "currency": invoice.currency,
                "net_worth": invoice.net_worth,
                "vat_total": invoice.vat_total,
                "gross_worth": invoice.gross_worth,
                "pdf_path": invoice.pdf_path,
                "extracted_at": invoice.extracted_at
            }
            conn.execute(invoice_stmt, invoice_params)
            
            items_ids = [str(uuid4()) for _ in items]
            items_params = [
                {
                    "id": items_ids[i],
                    "line_no": item.line_no,
                    "description": item.description,
                    "quantity": item.quantity,
                    "net_price": item.net_price,
                    "gross_worth": item.gross_worth,
                    "net_worth": item.net_worth,
                    "vat": item.vat,
                    "invoice_id": invoice_id
                }
                for i, item in enumerate(items)
            ]
            conn.execute(items_stmt, items_params)

    except Exception as e:
        print(f"Error inserting data: {e}")
        return {"success": False}
    return {"success": True}