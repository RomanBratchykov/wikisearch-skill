 name: wikisearch
 description: Analyze Wikipedia pageview data and generate graphs, chart metrics and summaries comparing articles, topics and languages.

 #Overview

 This skill analyzes Wikipedia pageview data.

 This skill requires Python 3.x and the dependencies declared in
 pyproject.toml.
 
 Use the project's configured environment.
 
 If Python is unavailable, inform the user that Python is required
 and provide the setup instructions.

 Agent responcible for:
 - understanding user requests
 - splitting requests into args
 - identifying requested topics, articles and languages
 - searching for one wikipedia article regarding on topic in one language to pass to the scripts for analysis
 - choosing date range and granularity for analysis when not specified by the user
 - passing arguments to the scripts
 - interpreting the results from the scripts
 - using the scripts for analysis based on user requests


 Scrtipts responsible for:
 - finding names of articles in different languages
 - retrieving JSON data from wikimedia API
 - analysing info using pandas and matplotlib
 - generating graphs and charts 
 - generating pdf reports with summaries and metrics

 Agent COULD NOT create new scripts or modify existing scripts. The agent is only responsible for executing the scripts in the /scripts folder with the correct arguments and interpreting the results.

 #Flow

 When user mentions wikipedia pageviews:
 - Agent will ask for the topics, articles and languages to analyze. 
 - If user provides all the required information, agent will pass the arguments to the scripts for analysis.
 - If user provides link to the article agent will extract article name and language and will ask for additional topics and languages to analyze.
 - If user do not provide links to articles agent should interpret the topics based on user input and search for required article in one language to analyze.
 - When agent interprets the topics and languages it will ask to confirm the topics and lunguages and if user want to add new topics and languages to analyze.
 


 #Execution rules

 All scripts should be executed in the /scripts folder

 DO NOT:
    - create new scripts.
    - modify existing scripts.


