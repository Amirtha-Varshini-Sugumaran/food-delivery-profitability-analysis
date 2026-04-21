# Power BI Model Notes

## Main Table

Use `food_delivery_cleaned_for_powerbi.csv` as the main fact table.

Recommended table name:

`Food Delivery Orders`

## Recommended Date Handling

Create a date table in Power BI and relate it to `order_datetime`.

Suggested DAX:

```DAX
Date = CALENDAR(MIN('Food Delivery Orders'[order_datetime]), MAX('Food Delivery Orders'[order_datetime]))
```

Add:

```DAX
Year = YEAR('Date'[Date])
Month = FORMAT('Date'[Date], "YYYY-MM")
Month Name = FORMAT('Date'[Date], "MMM")
```

## Recommended Relationships

For this portfolio project, a single-table model is acceptable because the dataset is already analysis-ready.

If expanding the model later, split dimensions into:

- City / Zone
- Restaurant
- Customer
- Date
- Acquisition Channel
- Discount Band

## Dashboard Design Note

Keep profit, delay rate, repeat rate, and rating visible together. The main story is that growth only matters if it is profitable and operationally reliable.

