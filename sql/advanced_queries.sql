-- Advanced analytical queries

WITH customer_metrics AS (
    SELECT customer_id, COUNT(*) AS orders, SUM(order_value) AS total_order_value,
           SUM(gross_profit) AS total_profit, AVG(profit_margin_pct) AS avg_margin_pct,
           AVG(delivery_delay_flag) AS delay_rate, AVG(repeat_customer_flag) AS repeat_rate
    FROM food_delivery_orders
    GROUP BY customer_id
), ranked AS (
    SELECT *, NTILE(4) OVER (ORDER BY total_profit) AS profit_quartile,
              NTILE(4) OVER (ORDER BY orders) AS frequency_quartile
    FROM customer_metrics
)
SELECT customer_id, orders, ROUND(total_profit, 2) AS total_profit,
       ROUND(avg_margin_pct, 2) AS avg_margin_pct,
       ROUND(delay_rate * 100, 2) AS delay_rate_pct,
       CASE
           WHEN profit_quartile = 4 AND frequency_quartile >= 3 THEN 'High-value loyal'
           WHEN profit_quartile <= 2 AND frequency_quartile = 4 THEN 'High-volume low-margin'
           WHEN profit_quartile = 4 THEN 'High-profit occasional'
           ELSE 'Standard'
       END AS customer_segment
FROM ranked
ORDER BY total_profit DESC;

WITH restaurant_zone AS (
    SELECT restaurant_id, city, zone, cuisine_type, COUNT(*) AS orders,
           SUM(gross_profit) AS profit, AVG(delivery_delay_flag) AS delay_rate,
           AVG(rating) AS avg_rating, AVG(refund_amount) AS avg_refund
    FROM food_delivery_orders
    GROUP BY restaurant_id, city, zone, cuisine_type
    HAVING COUNT(*) >= 8
)
SELECT *,
       RANK() OVER (PARTITION BY city ORDER BY delay_rate DESC, avg_rating ASC) AS city_risk_rank,
       RANK() OVER (PARTITION BY city ORDER BY profit DESC) AS city_profit_rank
FROM restaurant_zone
ORDER BY city, city_risk_rank;

WITH monthly AS (
    SELECT order_month, COUNT(*) AS orders, SUM(gross_profit) AS gross_profit,
           AVG(profit_margin_pct) AS avg_margin_pct
    FROM food_delivery_orders
    GROUP BY order_month
)
SELECT order_month, orders, ROUND(gross_profit, 2) AS gross_profit,
       ROUND(avg_margin_pct, 2) AS avg_margin_pct,
       ROUND(gross_profit - LAG(gross_profit) OVER (ORDER BY order_month), 2) AS profit_change_vs_previous_month
FROM monthly
ORDER BY order_month;
