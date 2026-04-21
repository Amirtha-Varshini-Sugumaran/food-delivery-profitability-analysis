-- Core business queries

-- Profitability by city and cuisine
SELECT city, cuisine_type, COUNT(*) AS orders,
       ROUND(SUM(gross_profit), 2) AS total_gross_profit,
       ROUND(AVG(profit_margin_pct), 2) AS avg_margin_pct,
       ROUND(AVG(order_value), 2) AS avg_order_value
FROM food_delivery_orders
GROUP BY city, cuisine_type
ORDER BY total_gross_profit DESC;

-- Discount impact on repeat behaviour
SELECT discount_band, COUNT(*) AS orders,
       ROUND(AVG(discount_amount), 2) AS avg_discount,
       ROUND(AVG(gross_profit), 2) AS avg_profit,
       ROUND(AVG(repeat_customer_flag) * 100, 2) AS repeat_rate_pct
FROM food_delivery_orders
GROUP BY discount_band
ORDER BY avg_discount;

-- Late delivery patterns
SELECT city, zone, COUNT(*) AS orders,
       ROUND(AVG(delivery_delay_flag) * 100, 2) AS delay_rate_pct,
       ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
       ROUND(AVG(rating), 2) AS avg_rating
FROM food_delivery_orders
GROUP BY city, zone
HAVING COUNT(*) >= 30
ORDER BY delay_rate_pct DESC, avg_rating ASC;

-- Restaurant performance
SELECT restaurant_id, city, zone, cuisine_type, COUNT(*) AS orders,
       ROUND(SUM(gross_profit), 2) AS total_profit,
       ROUND(AVG(delivery_delay_flag) * 100, 2) AS delay_rate_pct,
       ROUND(AVG(rating), 2) AS avg_rating
FROM food_delivery_orders
GROUP BY restaurant_id, city, zone, cuisine_type
HAVING COUNT(*) >= 8
ORDER BY total_profit DESC;

-- Customer tenure and profit quality
SELECT customer_tenure_group, COUNT(*) AS orders, COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(gross_profit), 2) AS total_profit,
       ROUND(AVG(gross_profit), 2) AS avg_profit_per_order,
       ROUND(AVG(repeat_customer_flag) * 100, 2) AS repeat_rate_pct
FROM food_delivery_orders
GROUP BY customer_tenure_group
ORDER BY total_profit DESC;
