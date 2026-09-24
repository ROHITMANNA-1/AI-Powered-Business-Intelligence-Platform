# Power BI Dashboard Guide

## Connection and model

1. Load `data/processed/cleaned_data.csv` with **Get Data > Text/CSV**, or connect to the MySQL `analysis_data` table.
2. Set `invoice_date` to Date/Time and `revenue` to Decimal Number.
3. If a calendar table is needed, create one with the DAX below and relate `Calendar[Date]` to `analysis_data[invoice_date]` at date grain.
4. Do not publish credentials or the local `.env` file.

```DAX
Calendar = CALENDAR(MIN(analysis_data[invoice_date]), MAX(analysis_data[invoice_date]))
Year = YEAR(Calendar[Date])
Month = FORMAT(Calendar[Date], "YYYY-MM")
```

## Measures

```DAX
Total Revenue = SUM(analysis_data[revenue])
Orders = DISTINCTCOUNT(analysis_data[invoice_no])
Customers = DISTINCTCOUNT(analysis_data[customer_id])
Average Order Value = DIVIDE([Total Revenue], [Orders])
Units Sold = SUM(analysis_data[quantity])
Revenue per Customer = DIVIDE([Total Revenue], [Customers])

Revenue Previous Month =
CALCULATE([Total Revenue], DATEADD(Calendar[Date], -1, MONTH))

Revenue MoM Change = [Total Revenue] - [Revenue Previous Month]

Revenue MoM % = DIVIDE([Revenue MoM Change], [Revenue Previous Month])
```

Profit, profit margin, discount, delivery, and shipping measures are intentionally absent because the selected UCI source does not contain those fields.

## Pages

- **Executive overview:** Total Revenue, Orders, Customers, Average Order Value, monthly revenue line chart, country slicer, date slicer.
- **Sales and time:** monthly revenue, units sold, month-over-month change, drill-through to invoice details.
- **Product and geography:** revenue by description, country map/table, top-product table.
- **Customer analysis:** customer revenue distribution, repeat customer count, top customers. Use only when `customer_id` completeness is acceptable.

Streamlit does not control Power BI. Refresh and sharing are managed in Power BI separately.
