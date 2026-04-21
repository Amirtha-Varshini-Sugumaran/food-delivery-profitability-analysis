# Data Dictionary

The dataset is synthetic but built to behave like food delivery operating data. The raw file intentionally includes duplicated orders, inconsistent city and payment labels, missing ratings, missing driver IDs, blank discounts, mixed timestamp formats, and delivery-time outliers.

| Field | Definition |
|---|---|
| order_id | Unique order reference. Raw data includes duplicated rows for some orders. |
| customer_id | Customer identifier used for retention and segmentation. |
| restaurant_id | Restaurant identifier used for restaurant performance analysis. |
| city | Operating city. Raw data includes inconsistent casing and Delhi NCR variants. |
| zone | Local operating zone within a city. |
| cuisine_type | Restaurant cuisine category. |
| order_datetime | Order timestamp. Raw data includes two timestamp formats. |
| delivery_partner_id | Driver assigned to the order. Some raw rows are missing this. |
| delivery_time_minutes | Actual delivery time in minutes. Includes a small number of outliers. |
| promised_delivery_time_minutes | Customer promise time in minutes. |
| delivery_delay_flag | 1 when actual time is greater than promised time. |
| order_value | Basket value before charges, discounts, and refunds. |
| delivery_fee | Delivery fee charged to the customer. |
| discount_amount | Promotional discount. Some raw rows are blank. |
| packaging_charge | Packaging charge included on the order. |
| platform_commission | Commission earned from the restaurant. |
| refund_amount | Refund linked to cancellation or service issue. |
| rating | Customer rating from 1 to 5. Some raw rows are missing. |
| payment_method | Payment method. Raw data includes inconsistent labels. |
| customer_tenure_group | Customer age group with the platform. |
| repeat_customer_flag | 1 if the customer shows repeat behaviour after this order. |
| acquisition_channel | Customer acquisition source. |
| order_status | Delivered, cancelled, or refunded. |
| distance_km | Delivery distance in kilometres. |
| weather_condition | Weather during delivery. |
| weekend_flag | 1 for Saturday or Sunday orders. |
| festival_flag | 1 for festival or high-demand period orders. |
| gross_profit | Commission plus fees and packaging, less discounts and refunds. |
| profit_margin_pct | Gross profit divided by order value. |
| delay_minutes | Minutes beyond promised delivery time. |
| discount_band | No Discount, Low, Medium, or High. |
| order_month | Month extracted from order timestamp. |
