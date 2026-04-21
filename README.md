# Food Delivery Profitability, Customer Retention, and Operational Performance Analysis

## Project Snapshot

End-to-end data analytics project for a fast-growing food delivery platform operating across major Indian cities. The analysis reviews profitability, discount efficiency, customer retention, delivery delays, ratings, and restaurant-zone performance.

The project is designed for quick recruiter review: it includes cleaned and raw datasets, Python analysis, SQL queries, Excel workbook outputs, Power BI-ready files, and business recommendations.

## Business Problem

The platform has strong growth, but not every order is equally valuable. Some customers order often but only with high discounts. Some restaurant and zone combinations create repeated delays. Late deliveries appear to reduce ratings, and lower ratings can weaken repeat behaviour.

## Business Value

This project shows how a data analyst can turn messy operating data into practical decisions for commercial, operations, and customer teams. The analysis focuses on where the company earns margin, where discounts may be wasteful, and which delivery issues should be fixed first.

## Data Source

The dataset is synthetic and was created for this portfolio case study. It is designed to behave like realistic food delivery operating data, with order-level revenue, discount, delivery, customer, restaurant, rating, and repeat-order fields. This approach keeps the project public and shareable while still allowing meaningful cleaning, analysis, SQL, Excel, and Power BI work.

## Tools Used

- Python for cleaning, wrangling, EDA, statistics, segmentation, and ML basics
- SQL for repeatable business analysis
- Power BI for dashboard design and Power BI-ready reporting files
- Excel for validation, pivots, KPI review, and workbook analysis
- GitHub for project packaging

## Key Outputs

- Excel workbook: `excel/food_delivery_profitability_workbook.xlsx`
- Power BI-ready dataset: `powerbi/powerbi_ready_files/food_delivery_cleaned_for_powerbi.csv`
- Main Python analysis file: `scripts/05_full_python_analysis.py`
- Supporting Python scripts: `scripts/`
- Jupyter notebooks: `notebooks/`
- SQL analysis: `sql/`
- Business insights and recommendations: `insights/`

## Repository Structure

```text
food-delivery-profitability-analysis/
|-- data/
|-- notebooks/
|-- scripts/
|-- sql/
|-- powerbi/
|-- excel/
|-- insights/
|-- artifacts/
```

## Key Questions Answered

- Which customers and segments drive profit, not just order volume?
- Are discounts improving retention or mainly reducing margins?
- Which city, zone, cuisine, and restaurant patterns create delivery problems?
- Are late deliveries linked with lower ratings and weaker repeat behaviour?
- Which actions should operations and commercial teams prioritise first?

## Project Workflow

1. Create and review a realistic messy order dataset.
2. Clean duplicate rows, inconsistent categories, missing values, timestamps, and outliers.
3. Engineer profit, delay, discount, and customer behaviour features.
4. Analyse profitability, delivery performance, discount impact, and retention patterns.
5. Use practical statistics to test whether observed differences matter.
6. Build customer segmentation and retention logic.
7. Train a simple repeat-order prediction model.
8. Translate findings into Power BI, Excel, and leadership-ready recommendations.

## Highlights Of Findings

- High discounts improve repeat behaviour only slightly in some groups, but often reduce profit margin.
- Delayed deliveries are linked with lower ratings, especially in dense urban zones and bad weather.
- High-frequency customers do not always create high profit.
- Restaurant-zone combinations are more useful for operations than restaurant rankings alone.
- Repeat behaviour is best understood by looking at tenure, rating, discount pattern, profit quality, and delivery reliability together.

## Skills Demonstrated

- Data cleaning and wrangling
- Python analysis and reusable scripts
- SQL business analysis
- Excel workbook reporting
- Power BI dashboard planning
- KPI design
- Statistical reasoning
- Customer segmentation
- Basic machine learning for repeat-order prediction
- Business storytelling and recommendations

## Quick Review Path

1. Start with `insights/executive_summary.md`.
2. Open `excel/food_delivery_profitability_workbook.xlsx` for KPI and workbook output.
3. Review `scripts/05_full_python_analysis.py` for the main Python analysis.
4. Check `sql/analysis_queries.sql` and `sql/advanced_queries.sql` for SQL depth.
5. Use `powerbi/powerbi_ready_files/food_delivery_cleaned_for_powerbi.csv` as the source for the Power BI `.pbix` dashboard.
