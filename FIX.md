# Fix instructions
 
Apply the fixes below to `data_request.py`. Do not rewrite, refactor, rename,
or restructure anything else in the file. Do not change function signatures,
CLI arguments, or unrelated logic. Only touch what is listed.
 
## 1. `calculate_statistics` — wrong `period_size` for daily granularity
 
Current:
```python
if granularity == "daily":
    period_size = 24 * 30
elif granularity == "monthly":
    period_size = 12
```
 
Problem: for daily granularity each row is one day, not one hour, so
`period_size` is inflated to 720. `views.iloc[:period_size]` and
`views.iloc[-period_size:]` silently clamp to the full series when it has
fewer than 720 rows, so `first_period == last_period` and
`growth_percent` comes out as 0 for any fetch shorter than ~2 years.
 
Fix: change the row counts to represent actual comparison windows in rows,
not hours:
```python
if granularity == "daily":
    period_size = 30
elif granularity == "monthly":
    period_size = 3
```
 
## 2. `calculate_statistics` — overlapping windows on short series
 
Add a guard before computing `first_period`/`last_period`: if
`len(dataframe) < 2 * period_size`, shrink `period_size` to
`len(dataframe) // 2` so the two windows never overlap. If the resulting
`period_size` is 0 (series too short to compare), set `growth_percent` to
`None` instead of computing it, and skip division.
 
## 3. `calculate_statistics` — division by zero / near-zero `first_period`
 
Current:
```python
"growth_percent": float(
    (last_period - first_period) / first_period * 100
),
```
 
Guard against `first_period == 0` (or NaN): if so, set `growth_percent`
to `None` instead of raising or producing `inf`/`nan`. Otherwise compute
as before.