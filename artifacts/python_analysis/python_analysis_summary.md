# Python Analysis Summary

## KPI Snapshot

| KPI | Value |
|---|---:|
| Total Orders | 3,200 |
| Gross Profit | INR 327,872.00 |
| Average Order Value | INR 454.76 |
| Average Margin % | 26.38% |
| Repeat Rate % | 45.06% |
| Delay Rate % | 76.62% |
| Average Rating | 3.78 |
| Total Discount | INR 149,951.93 |

## Main Findings

- Highest-profit cities are not automatically the cleanest operational markets. Profit needs to be reviewed with delay rate and rating.
- Discount bands show different repeat behaviour, but the repeat lift should be compared against margin loss.
- Delayed orders have a lower average rating than on-time orders.
- The approximate p-value for the delayed vs on-time rating difference is 0.000000, which supports treating delay as a customer experience issue.
- Customer segmentation separates high-value loyal customers from high-volume low-margin customers.
- The repeat-order scorecard accuracy is 63.91%. It is useful for prioritisation, not automated decision-making.

## Chart Output

Chart PNGs were skipped because matplotlib is not installed in this local runtime. The CSV outputs are still created and can be charted in Power BI or Excel.

## Files Created By This Script

- `artifacts/python_analysis/city_profitability_summary.csv`
- `artifacts/python_analysis/discount_retention_summary.csv`
- `artifacts/python_analysis/top_zone_risk_summary.csv`
- `artifacts/python_analysis/customer_segment_summary.csv`
- `artifacts/python_analysis/repeat_score_sample.csv`
- `artifacts/python_analysis/figures/gross_profit_by_city.png`
- `artifacts/python_analysis/figures/repeat_rate_by_discount_band.png`
- `artifacts/python_analysis/figures/top_delay_hotspots.png`
