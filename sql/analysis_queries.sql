-- KPI definitions used by the application and Power BI.
SELECT SUM(revenue) AS total_revenue FROM analysis_data;
SELECT COUNT(DISTINCT invoice_no) AS orders FROM analysis_data;
SELECT COUNT(DISTINCT customer_id) AS customers FROM analysis_data WHERE customer_id IS NOT NULL;
SELECT SUM(revenue) / NULLIF(COUNT(DISTINCT invoice_no), 0) AS average_order_value FROM analysis_data;
SELECT country, SUM(revenue) AS revenue FROM analysis_data GROUP BY country ORDER BY revenue DESC;
SELECT DATE_FORMAT(invoice_date, '%Y-%m') AS month, SUM(revenue) AS revenue FROM analysis_data GROUP BY month ORDER BY month;
