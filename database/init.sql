-- MySQL schema for extracted invoice data
-- Only DDL: create database + tables (no inserts)

CREATE DATABASE IF NOT EXISTS grocery_agent_db
	CHARACTER SET utf8mb4
	COLLATE utf8mb4_0900_ai_ci;

USE grocery_agent_db;

CREATE TABLE IF NOT EXISTS users (
	id VARCHAR(36) NOT NULL,
	name VARCHAR(255) NOT NULL,
	tax_id VARCHAR(64) NULL,
	iban VARCHAR(64) NULL,
	address VARCHAR(512) NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	UNIQUE KEY uq_users_tax_id (tax_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS invoices (
	id VARCHAR(36) NOT NULL,
	invoice_number VARCHAR(128) NOT NULL,
	issue_date DATE NULL,
	seller_id VARCHAR(36) NOT NULL,
	client_id VARCHAR(36) NOT NULL,
	currency CHAR(3) NULL,
	net_worth DECIMAL(15,2) NOT NULL DEFAULT 0.00,
	vat_total DECIMAL(15,2) NOT NULL DEFAULT 0.00,
	gross_worth DECIMAL(15,2) NOT NULL DEFAULT 0.00,
	pdf_path VARCHAR(1024) NULL,
	extracted_at DATETIME(6) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	KEY idx_invoices_issue_date (issue_date),
	KEY idx_invoices_seller (seller_id),
	KEY idx_invoices_client (client_id),
	CONSTRAINT fk_invoices_seller
		FOREIGN KEY (seller_id) REFERENCES users(id)
		ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT fk_invoices_client
		FOREIGN KEY (client_id) REFERENCES users(id)
		ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS invoice_detail (
	id VARCHAR(36) NOT NULL,
	description VARCHAR(512) NOT NULL,
	gross_worth DECIMAL(15,2) NOT NULL DEFAULT 0.00,
	line_no INT NOT NULL,
	net_price DECIMAL(15,4) NOT NULL DEFAULT 0.0000,
	net_worth DECIMAL(15,2) NOT NULL DEFAULT 0.00,
	quantity INT NOT NULL DEFAULT 1,
	vat DECIMAL(15,2) NOT NULL DEFAULT 0.00,
	invoice_id VARCHAR(36) NOT NULL,
	PRIMARY KEY (id),
	KEY idx_invoice_detail_invoice_id (invoice_id),
	CONSTRAINT fk_invoice_detail_invoice
		FOREIGN KEY (invoice_id) REFERENCES invoices(id)
		ON UPDATE RESTRICT ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
