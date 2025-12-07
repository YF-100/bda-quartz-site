---
title: SUMMARY
---

# Evidence Summary

## Execution Plans
- `plan_q1.txt` — Q1 filter + count
- `plan_q2.txt` — Q2 reduce-side join
- `plan_q3.txt` — Q3 broadcast join
- `plan_q5.txt` — Q5 time series aggregation
- `plan_ppr.txt` — Sample physical plan

## Spark UI Screenshots
Captured screenshots showing Spark UI metrics:
- `ui_q1_filter.png` — Q1 filter + count stage
- `ui_q2_join.png` — Q2 reduce-side join stage
- `ui_q3_broadcast.png` — Q3 broadcast join stage
- `ui_q4_agg.png` — Q4 aggregation stage
- `ui_q5_timeseries.png` — Q5 time series aggregation stage
- `ui_hourly_stream.png` — HourlyTripCount streaming job
- `ui_region_stream.png` — RegionTripCount streaming job
- `ui_trending_stream.png` — TrendingArrivals streaming job

Each screenshot includes:
- Files Read
- Input Size
- Shuffle Read/Write
- Task metrics

## Performance Notes
See `PERFORMANCE_NOTES.md` in root directory for detailed analysis.

## What to Submit
1. All `plan_*.txt` files
2. UI screenshots (at least one per major query type)
3. ENV.md
4. This summary
5. Notebook with executed output
