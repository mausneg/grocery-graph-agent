from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
from sqlalchemy import text
from uuid import uuid4
from datetime import datetime

from app.state import InvoiceState
from app.database import db

load_dotenv()

def insert_data(state: InvoiceState):
    print("Inserting data into database...")
    invoice = state["invoice"]

    def parse_date(value: str | None):
        if not value:
            return None
        value = str(value).strip()
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%m-%d-%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(value).date()
        except Exception:
            return None

    def parse_datetime(value: str | None):
        if not value:
            return datetime.now()
        value = str(value).strip()
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return datetime.now()

    def get_or_create_user(conn, *, name: str, tax_id: str | None, iban: str | None, address: str | None) -> str:
        tax_id_clean = (tax_id or "").strip() or None
        if tax_id_clean:
            existing = conn.execute(
                text("SELECT id FROM users WHERE tax_id = :tax_id LIMIT 1"),
                {"tax_id": tax_id_clean},
            ).fetchone()
            if existing and existing[0]:
                return str(existing[0])

        new_id = str(uuid4())
        conn.execute(
            text(
                """
                INSERT INTO users (id, name, tax_id, iban, address, created_at)
                VALUES (:id, :name, :tax_id, :iban, :address, NOW())
                """
            ),
            {
                "id": new_id,
                "name": name,
                "tax_id": tax_id_clean,
                "iban": iban,
                "address": address,
            },
        )
        return new_id

    client = invoice.client
    seller = invoice.seller
    items = invoice.invoice_items
    invoice_id = str(uuid4())

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
            client_id = get_or_create_user(
                conn,
                name=client.name,
                tax_id=getattr(client, "tax_id", None),
                iban=getattr(client, "iban", None),
                address=getattr(client, "address", None),
            )
            seller_id = get_or_create_user(
                conn,
                name=seller.name,
                tax_id=getattr(seller, "tax_id", None),
                iban=getattr(seller, "iban", None),
                address=getattr(seller, "address", None),
            )

            invoice_params = {
                "id": invoice_id,
                "invoice_number": invoice.invoice_number,
                "issue_date": parse_date(getattr(invoice, "issue_date", None)),
                "seller_id": seller_id,
                "client_id": client_id,
                "currency": invoice.currency,
                "net_worth": invoice.net_worth,
                "vat_total": invoice.vat_total,
                "gross_worth": invoice.gross_worth,
                "pdf_path": state.get("data_path") or getattr(invoice, "pdf_path", None),
                "extracted_at": parse_datetime(getattr(invoice, "extracted_at", None)),
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
        return {"success": False, "error_message": str(e)}
    return {"success": True, "invoice_id": invoice_id}