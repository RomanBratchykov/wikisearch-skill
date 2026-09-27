---
 name: wikisearch-skill
 description: Analyze Wikipedia pageview data and generate graphs, chart metrics and summaries comparing articles, topics and languages.
 allowed-tools:
   - Bash(rtk ls:*)
   - Bash(uv sync:*)
   - Bash(rtk uv run:*)
---

 # Overview

 This skill analyzes Wikipedia pageview data.

 Agent responsible for:
 - searhing of files in the skills folder
 - understanding user requests
 - splitting requests into args
 - identifying requested topics, articles and languages
 - searching for one wikipedia article regarding on topic in one language to pass to the scripts 
 - choosing date range and granularity for analysis when not specified by the user
 - passing arguments to the scripts
 - interpreting the results from the scripts
 - using the scripts for analysis based on user requests without asking for permission
 -creating json summary of output/analysis.json to be used for pdf and graph generation with LLM to summarize the data and generate metrics. The report should include:
   - Summary of pageviews for each article and language
   - Comparison metrics based on user-specified criteria
   - Any notable trends or insights
   - file should be generated in 'output/report.json'


  Scripts responsible for:
 - finding names of articles in different languages
 - retrieving JSON data from wikimedia API
 - analysing info using pandas and matplotlib
 - generating graphs and charts 
 - generating pdf reports with summaries and metrics

 Agent should NOT create new scripts or modify existing scripts. The agent is only responsible for executing the scripts in the /scripts folder with the correct arguments and interpreting the results.


 ## Environment

The skill MUST NOT modify the user's system environment or install packages automatically.

The skill requires the project's reproducible Python environment defined by
`pyproject.toml` and `uv.lock`.

For initial environment setup, run:

```bash
uv sync
```
and inform the user, that you will use the project's configured environment.

 # Flow

 When user mentions wikipedia pageviews:

1. Understand the requested:
   - topic/article
   - Wikipedia languages
   - date range
   - granularity
   - comparison criteria
   - requested output

2. Fetch pageview data using:
   `uv run scripts/data_request.py fetch --languages "LANG1" "LANG2" ... --article "ART1"... --start "YYYYMMDDHH" --end "YYYYMMDDHH" --granularity "daily|monthly" --output "output/pageviews.json"`
    Do not manually translate article titles or search for each language separately when the language-link resolver can provide them. 

3. Analyze the data using:
   `uv run scripts/data_request.py analyze --input "output/pageviews.json" --output "output/analysis.json"`

4. Based on the 'output/analysis.json' generate json report that can be used both on pdf and graph generation using LLM to summarize the data and generate metrics. The report should include:
   - Summary of pageviews for each article and language
   - Comparison metrics based on user-specified criteria
   - Any notable trends or insights
file should be generated in 'output/report.json'

5. If requested, generate a PDF report with summaries and metrics using:
   `uv run scripts/pdf_converter.py --input "output/report.json" --output "output/report.pdf"`
   
6. If requested, generate graphs and charts using:
   `uv run scripts/graph_builder.py --input "output/report.json" --output "output/graphs.png"`

 #Execution rules

 All scripts should be executed in the /scripts folder


 DO NOT:
    - create new scripts.
    - modify existing scripts.
    - manually translate article titles or search for each language separately when the language-link resolver can provide them.
    - manually fetch data from the Wikimedia API when the `fetch_data_page()` script can do it.
    - manually analyze data when the `analyze_data()` script can do it.
    - manually generate graphs and charts when the `build_graph()` script can do it.
    - manually generate PDF reports when the `convert_to_pdf()` script can do it.
    - install Python packages or dependencies globally.
    - use the LLM to process large raw datasets when deterministic Python processing is available
    - ask user if agent can check files in system or to create .json, .pdf or .png files in the output folder.
    - ask user if agent can run scripts in the /scripts folder

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
