# Measures And Dimensions

## Core KPIs

| Measure | Definition |
|---|---|
| Total Orders | Count of order_id |
| Gross Profit | Sum of gross_profit |
| Average Margin % | Average of profit_margin_pct |
| Average Order Value | Average of order_value |
| Total Discount | Sum of discount_amount |
| Discount Rate % | Total discount divided by total order value |
| Repeat Rate % | Average of repeat_customer_flag |
| Delay Rate % | Average of delivery_delay_flag |
| Average Delay Minutes | Average of delay_minutes |
| Average Rating | Average of rating |

## DAX Ideas

```DAX
Gross Profit = SUM(food_delivery_orders[gross_profit])
Delay Rate % = AVERAGE(food_delivery_orders[delivery_delay_flag])
Repeat Rate % = AVERAGE(food_delivery_orders[repeat_customer_flag])
Discount Rate % = DIVIDE(SUM(food_delivery_orders[discount_amount]), SUM(food_delivery_orders[order_value]))
Profit Per Order = DIVIDE([Gross Profit], [Total Orders])
```

## Dimensions And Filters

Date/month, city, zone, cuisine type, restaurant, customer tenure group, discount band, acquisition channel, weather condition, weekend flag, festival flag, payment method, and order status.
