--  Remove duplicate rows from the sales table
DELETE FROM sales
WHERE id NOT IN (
    SELECT MIN(id)
    FROM sales
    GROUP BY sale_date, company_name, total_sales, web_traffic, advertising_spend, customer_review_score, social_media_mentions
);

--  Handle NULL values in key columns
UPDATE sales
SET 
    web_traffic = COALESCE(web_traffic, 0), -- Replace NULL web traffic with 0
    advertising_spend = COALESCE(advertising_spend, 0), -- Replace NULL ad spend with 0
    customer_review_score = COALESCE(customer_review_score, 3.0); -- Default average review score

-- Calculate and insert KPIs into the kpi_metrics table
INSERT INTO kpi_metrics (company_name, average_ticket_size, conversion_rate, total_sales, average_web_traffic)
SELECT 
    company_name,
    AVG(total_sales / NULLIF(web_traffic, 0)) AS average_ticket_size, -- Avg sales per web visit
    SUM(total_sales) / NULLIF(SUM(web_traffic), 0) AS conversion_rate, -- Conversion rate
    SUM(total_sales) AS total_sales, -- Total sales for the company
    AVG(web_traffic) AS average_web_traffic -- Average web traffic
FROM sales
GROUP BY company_name;

-- Normalize KPIs for easier visualization
UPDATE kpi_metrics
SET 
    average_ticket_size = average_ticket_size / (SELECT MAX(average_ticket_size) FROM kpi_metrics), -- Normalize avg ticket size
    conversion_rate = conversion_rate / (SELECT MAX(conversion_rate) FROM kpi_metrics); -- Normalize conversion rate
