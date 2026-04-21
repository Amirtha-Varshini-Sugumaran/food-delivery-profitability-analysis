# Power BI Dashboard Files

This folder contains Power BI-ready files and a dashboard specification.

## Important Note

A native `.pbix` file must be created in Power BI Desktop. This repository includes the cleaned dataset, KPI definitions, dashboard page design, and a Power BI-ready CSV package so the dashboard can be built quickly and consistently.

## Files To Use

- `powerbi_ready_files/food_delivery_cleaned_for_powerbi.csv`
- `dashboard_spec.md`
- `measures_and_dimensions.md`
- `powerbi_model_notes.md`

## Suggested Power BI Build

1. Open Power BI Desktop.
2. Select `Get Data > Text/CSV`.
3. Load `powerbi_ready_files/food_delivery_cleaned_for_powerbi.csv`.
4. Set `order_datetime` as Date/Time.
5. Create the measures listed in `measures_and_dimensions.md`.
6. Build four pages:
   - Executive Overview
   - Profitability
   - Delivery Performance
   - Customer Retention

