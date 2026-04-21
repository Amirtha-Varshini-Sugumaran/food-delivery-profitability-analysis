# Food Delivery Profitability, Customer Retention, and Operational Performance Analysis

## Short Summary

This project analyses a fast-growing food delivery platform operating across major Indian cities, with a practical expansion lens that would also be useful for reviewing a smaller Irish market launch.

The company has grown order volume quickly, but leadership now needs a clearer view of profit quality, discount efficiency, delivery reliability, and retention. The analysis looks beyond order counts and asks where the company is actually making money, where discounts are leaking margin, and where operational problems are likely to damage repeat behaviour.

## Business Problem

The platform has strong growth, but not every order is equally valuable. Some customers order often but only with high discounts. Some restaurant and zone combinations create repeated delays. Late deliveries appear to reduce ratings, and lower ratings can weaken repeat behaviour.

## Why This Project Matters

This is the kind of analysis a delivery platform needs once growth starts becoming expensive. It combines Python, SQL, Excel checks, Power BI planning, statistics, segmentation, and a simple machine learning model.

## Tools Used

- Python for cleaning, wrangling, EDA, statistics, segmentation, and ML basics
- SQL for repeatable business analysis
- Power BI for dashboard design and Power BI-ready reporting files
- Excel for validation, pivots, KPI review, and workbook analysis
- GitHub for project packaging

## Main Deliverables

- Excel workbook: `excel/food_delivery_profitability_workbook.xlsx`
- Power BI-ready dataset: `powerbi/powerbi_ready_files/food_delivery_cleaned_for_powerbi.csv`
- Power BI build guide: `powerbi/README_POWERBI.md`
- Python scripts: `scripts/`
- Jupyter notebooks: `notebooks/`
- SQL analysis: `sql/`

## Repository Structure

```text
food-delivery-profitability-analysis/
├── data/
├── notebooks/
├── scripts/
├── sql/
├── powerbi/
├── excel/
├── insights/
├── artifacts/
└── local_only/
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

## How To Use This Project In Interviews

Use this project to show the full analysis lifecycle. Start with the business problem, then explain how you cleaned messy delivery data, created profitability and delay features, used SQL to answer business questions, applied statistics to test assumptions, designed a Power BI dashboard, and built a simple ML model for repeat order prediction.
