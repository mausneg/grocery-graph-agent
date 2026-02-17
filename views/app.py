from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

import streamlit as st

from app.graph_data import graph_data
from app.graph_query import graph_query


APP_TITLE = "Invoice Assistant"
UPLOAD_DIR = Path("data/uploads")


def _init_state() -> None:
	if "messages" not in st.session_state:
		st.session_state["messages"] = []
	if "last_ingest_state" not in st.session_state:
		st.session_state["last_ingest_state"] = None
	if "last_pdf_path" not in st.session_state:
		st.session_state["last_pdf_path"] = None
	if "last_query_state" not in st.session_state:
		st.session_state["last_query_state"] = None


def _safe_filename(filename: str) -> str:
	filename = filename.strip().replace("\\", "/").split("/")[-1]
	filename = re.sub(r"[^A-Za-z0-9._-]+", "_", filename)
	return filename or "upload.pdf"


def _save_upload(uploaded_file) -> Path:
	UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	safe_name = _safe_filename(getattr(uploaded_file, "name", "upload.pdf"))
	out_path = UPLOAD_DIR / f"{timestamp}__{safe_name}"
	out_path.write_bytes(uploaded_file.getbuffer())
	return out_path


def _display_invoice_summary(invoice) -> None:
	st.subheader("Extraction summary")

	def fmt(value, default: str = "-") -> str:
		if value is None:
			return default
		text = str(value).strip()
		return text if text else default

	def fmt_date(value) -> str:
		text = fmt(value)
		if text == "-":
			return text
		# Common cases: YYYY-MM-DD, ISO datetime, MM/DD/YYYY
		for candidate in (text, text[:10]):
			candidate = candidate.strip()
			if re.match(r"^\d{4}-\d{2}-\d{2}$", candidate):
				return candidate
			try:
				return datetime.fromisoformat(candidate.replace("Z", "+00:00")).date().isoformat()
			except Exception:
				pass
		try:
			return datetime.strptime(text, "%m/%d/%Y").date().isoformat()
		except Exception:
			return text

	def fmt_number(value) -> str:
		try:
			return f"{float(value):,.2f}" if value is not None and str(value).strip() != "" else "-"
		except Exception:
			return fmt(value)

	try:
		seller = getattr(invoice, "seller", None)
		client = getattr(invoice, "client", None)

		left, right = st.columns([1, 1])
		with left:
			st.caption("Invoice number")
			st.code(fmt(getattr(invoice, "invoice_number", None)), language="text")
			m1, m2 = st.columns(2)
			with m1:
				st.caption("Issue date")
				st.write(fmt_date(getattr(invoice, "issue_date", None)))
			with m2:
				st.caption("Currency")
				st.write(fmt(getattr(invoice, "currency", None)))

			st.caption("Seller")
			st.write(fmt(getattr(seller, "name", None)))
			st.caption("Client")
			st.write(fmt(getattr(client, "name", None)))

		with right:
			t1, t2, t3 = st.columns(3)
			with t1:
				st.caption("Net")
				st.write(fmt_number(getattr(invoice, "net_worth", None)))
			with t2:
				st.caption("VAT")
				st.write(fmt_number(getattr(invoice, "vat_total", None)))
			with t3:
				st.caption("Gross")
				st.write(fmt_number(getattr(invoice, "gross_worth", None)))

		items = getattr(invoice, "invoice_items", []) or []
		if items:
			st.markdown("**Line items (preview)**")
			rows = []
			for item in items[:10]:
				rows.append(
					{
						"Line": getattr(item, "line_no", ""),
						"Description": getattr(item, "description", ""),
						"Qty": getattr(item, "quantity", ""),
						"Net price": getattr(item, "net_price", ""),
						"Net worth": getattr(item, "net_worth", ""),
						"VAT": getattr(item, "vat", ""),
						"Gross worth": getattr(item, "gross_worth", ""),
					}
				)
			st.dataframe(rows, use_container_width=True, hide_index=True)
			if len(items) > 10:
				st.caption("Showing first 10 items.")
	except Exception:
		st.write("Summary is not available.")


def _render_query_details(state: dict) -> None:
	query = state.get("query") or ""
	result = state.get("result") or ""
	error_message = state.get("error_message") or ""
	is_dangerous = bool(state.get("is_dangerous"))

	status_left, status_right = st.columns(2)
	if is_dangerous:
		status_left.warning("Blocked: only SELECT statements are allowed.")
	else:
		status_left.success("Query passed safety checks.")

	if error_message:
		status_right.error("Database execution error.")
	else:
		status_right.success("No execution error reported.")

	st.markdown("**Generated SQL**")
	st.code(str(query).strip(), language="sql")

	st.markdown("**Query result**")
	st.code(str(result).strip(), language="text")

	if error_message:
		st.markdown("**Error message**")
		st.code(str(error_message).strip(), language="text")


def main() -> None:
	st.set_page_config(page_title=APP_TITLE, layout="wide")
	_init_state()
	st.title(APP_TITLE)
	st.write(
		"Upload an invoice PDF to store it in the database, then ask questions in a chat format."
	)

	with st.sidebar:
		st.header("Invoice")
		uploaded = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=False)
		process = st.button("Process and store", type="primary", disabled=(uploaded is None))

		if process and uploaded is not None:
			try:
				saved_path = _save_upload(uploaded)
				with st.spinner("Memproses invoice..."):
					final_state = graph_data.invoke({"data_path": str(saved_path)})

				st.session_state["last_ingest_state"] = final_state
				st.session_state["last_pdf_path"] = str(saved_path)

				if final_state.get("success"):
					st.success("Processed and stored successfully.")
				else:
					msg = final_state.get("error_message") or "Failed to store data in the database."
					st.error(msg)
			except Exception as e:
				st.error("An error occurred while processing the file.")
				st.exception(e)

		last_pdf_path = st.session_state.get("last_pdf_path")
		if last_pdf_path:
			st.caption(f"Last processed: {last_pdf_path}")

		clear = st.button("Clear chat")
		if clear:
			st.session_state["messages"] = []
			st.session_state["last_query_state"] = None
			st.rerun()

		st.divider()
		st.subheader("Summary")
		last_ingest_state = st.session_state.get("last_ingest_state")
		if last_ingest_state and last_ingest_state.get("invoice") is not None:
			_display_invoice_summary(last_ingest_state.get("invoice"))
		else:
			st.caption("No invoice has been processed yet.")

	st.header("Chat")
	st.caption("Ask anything about the stored invoice data.")

	for msg in st.session_state["messages"]:
		with st.chat_message(msg["role"]):
			st.write(msg["content"])

	user_text = st.chat_input("Type your question")
	if user_text:
		st.session_state["messages"].append({"role": "user", "content": user_text})
		with st.chat_message("user"):
			st.write(user_text)

		with st.chat_message("assistant"):
			try:
				with st.spinner("Working..."):
					final_state = graph_query.invoke({"question": user_text.strip()})
				st.session_state["last_query_state"] = final_state

				raw_answer = final_state.get("answer")
				answer_text = getattr(raw_answer, "answer", None) or str(raw_answer or "")
				st.write(answer_text)
				st.session_state["messages"].append({"role": "assistant", "content": answer_text})
			except Exception as e:
				st.error("An error occurred while answering your question.")
				st.exception(e)

	last_query_state = st.session_state.get("last_query_state")
	if last_query_state:
		with st.expander("Technical details (optional)"):
			_render_query_details(last_query_state)

