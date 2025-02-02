-- Create raw sales table
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    sale_date DATE,
    company_name VARCHAR(50),
    total_sales NUMERIC,
    web_traffic INT,
    advertising_spend NUMERIC,
    customer_review_score FLOAT,
    social_media_mentions INT
);

-- Create KPI table
CREATE TABLE IF NOT EXISTS kpi_metrics (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(50),
    average_ticket_size NUMERIC,
    conversion_rate NUMERIC,
    total_sales NUMERIC,
    average_web_traffic NUMERIC
);
