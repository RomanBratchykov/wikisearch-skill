# wikisearch skill
 
Analyzes Wikipedia pageview data: fetches views per article/language,
computes stats, detects anomalies, and can render charts and a one-page
PDF report.

# Installation

use 

```bash
git clone https://github.com/RomanBratchykov/wikisearch-skill.git
cd wikisearch-skill
uv sync
```


## How it works
 
1. **fetch** — resolves the article's title in each requested language
   (via Wikipedia's language-links API), then pulls daily or monthly
   pageview counts for each language from the Wikimedia pageviews API.
   Result saved as raw JSON.
2. **analyze** — loads the raw JSON, computes per-language stats (total,
   average, median, min/max, volatility, growth %, peak day), flags
   anomalous days (z-score > 3), and keeps the full time series.
3. **graph_builder** — turns the analysis into charts.
4. **pdf_converter** — turns the analysis into a one-page shareable PDF.
## Usage
 
```bash
uv sync
 
# 1. fetch raw pageviews
uv run scripts/data_request.py fetch \
  --languages pl cs \
  --article "Intermittent fasting" \
  --start 2023010100 \
  --end 2024123100 \
  --granularity daily \
  --output output/pageviews.json
 
# 2. analyze
uv run scripts/data_request.py analyze \
  --input output/pageviews.json \
  --output output/analysis.json
```
 
Output of step 2 (`analysis.json`) contains, per language/article:
statistics, detected anomalies, and the full time series — ready for
charting or reporting.
 
## Notes / limitations
 
- Pageviews are a proxy for attention, not market size, unique users,
  or popularity outside Wikipedia.
- `growth_percent` compares the average of the first N rows vs the last
  N rows of the series (N = 30 for daily, 3 for monthly). On short
  series this window shrinks to avoid overlap; if the series is too
  short to compare two distinct periods, `growth_percent` is `None`.
- Bot traffic is excluded (`agent=user` in the API call).