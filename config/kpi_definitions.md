# KPI Definitions

These definitions are the contract for the Streamlit app, SQL examples, and Power BI measures.

| KPI | Definition | Required fields |
| --- | --- | --- |
| Total revenue | Sum of `quantity * unit_price` after configured cleaning | `quantity`, `unit_price` |
| Orders | Distinct count of `invoice_no` | `invoice_no` |
| Customers | Distinct count of non-null `customer_id` | `customer_id` |
| Average order value | Total revenue divided by distinct orders | Revenue and `invoice_no` |
| Units sold | Sum of `quantity` | `quantity` |
| Profit | Sum of source `profit`; never inferred from revenue | `profit` |
| Profit margin | Profit divided by revenue | `profit`, revenue |
| Delivery performance | On-time deliveries divided by deliveries with valid dates | Order and delivery dates |

The starter UCI dataset supports the first five measures. Profit, margin, discount, shipping, and delivery measures are unavailable unless present in an uploaded dataset.