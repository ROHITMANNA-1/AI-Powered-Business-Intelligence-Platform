-- MySQL schema for the normalized analysis table.
CREATE DATABASE IF NOT EXISTS ai_analyst;
USE ai_analyst;

CREATE TABLE IF NOT EXISTS analysis_data (
    invoice_no VARCHAR(32),
    stock_code VARCHAR(32),
    description TEXT,
    quantity INT,
    invoice_date DATETIME,
    unit_price DECIMAL(14, 4),
    customer_id VARCHAR(32),
    country VARCHAR(128),
    revenue DECIMAL(16, 4),
    INDEX idx_invoice_date (invoice_date),
    INDEX idx_customer_id (customer_id),
    INDEX idx_country (country)
);
