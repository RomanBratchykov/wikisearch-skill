 name: wikisearch
 description: Analyze Wikipedia pageview data and generate graphs, chart metrics and summaries comparing articles, topics and languages.

 # Overview

 This skill analyzes Wikipedia pageview data.

 Agent responsible for:
 - understanding user requests
 - splitting requests into args
 - identifying requested topics, articles and languages
 - searching for one wikipedia article regarding on topic in one language to pass to the scripts for analysis
 - choosing date range and granularity for analysis when not specified by the user
 - passing arguments to the scripts
 - interpreting the results from the scripts
 - using the scripts for analysis based on user requests

  Scripts responsible for:
 - finding names of articles in different languages
 - retrieving JSON data from wikimedia API
 - analysing info using pandas and matplotlib
 - generating graphs and charts 
 - generating pdf reports with summaries and metrics

 Agent COULD NOT create new scripts or modify existing scripts. The agent is only responsible for executing the scripts in the /scripts folder with the correct arguments and interpreting the results.


 ## Environment

The skill MUST NOT modify the user's system environment or install packages automatically.

The skill requires the project's reproducible Python environment defined by
`pyproject.toml` and `uv.lock`.

For initial environment setup, run:

```bash
uv sync
```
 # Flow

 When user mentions wikipedia pageviews:

1. Understand the requested:
   - topics/articles
   - Wikipedia languages
   - date range
   - granularity
   - comparison criteria
   - requested output

2. Fetch pageview data using:
   `uv run scripts/data_request.py fetch --languages "LANG1" "LANG2" ... --articles "ART1" "ART2" ... --start "YYYY-MM-DD" --end "YYYY-MM-DD" --granularity "daily|monthly" --output "pageviews.json"`
   Do not manually translate article titles or search for each language
   separately when the language-link resolver can provide them.

3. Analyze the data using:
   `uv run scripts/data_request.py analyze --input "pageviews.json" --output "analysis.json"`

4. If requested, generate graphs and charts using:
   `uv run scripts/output/graph_builder.py --input "analysis.json" --output "graph.png" --title "Pageviews" --xlabel "Date" --ylabel "Views"`

5. If requested, generate a PDF report with summaries and metrics using:
   `uv run scripts/output/pdf_converter.py --input "analysis.json" --output "report.pdf"`

 #Execution rules

 All scripts should be executed in the /scripts folder

 DO NOT:
    - create new scripts.
    - modify existing scripts.
    - manually translate article titles or search for each language separately when the language-link resolver can provide them.
    - manually fetch data from the Wikimedia API when the `fetch_data_page()` script can do it.
    - manually analyze data when the `analyze_data()` script can do it.
    - manually generate graphs and charts when the `generate_graphs()` script can do it.
    - manually generate PDF reports when the `generate_report()` script can do it.
    - install Python packages or dependencies globally.
    - use the LLM to process large raw datasets when deterministic Python
  processing is available

  Always use the scripts where possible, and only use the LLM for tasks that cannot be handled by the scripts.

 # Python dependencies

 This skill requires Python 3.x and the dependencies declared in
 pyproject.toml.
 
 Use the project's configured environment.
 
 If Python is unavailable, inform the user that Python is required
 and provide the setup instructions. 

 If the required environment is unavailable, report the missing
 dependency/environment and provide the project's documented setup command.

 # Defaults
 If user does not specify a date range, the default is the last 30 days.

 Default granularity is daily.

 If user does not specify a language, the default is English. 


 If user does not specify a comparison criteria, ask for it.

 If user does not specify output format ask for it.

 Always output all the analyzed answers as a written report in terminal 

 # Data interpretation

 Treat Wikipedia pageviews as a proxy for attention/interest.
 Do not interpret pageviews as:
 - market size
 - number of unique people
 - willingness to pay
 - popularity outside Wikipedia

 Separate measured statistics from interpretations.
