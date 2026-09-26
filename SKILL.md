 name: wikisearch
 description: A skill that allows you to analyze info about wikipedia articles views and generate graphs, metrics and summaries based on data. Each time user mention wikipedia, the skill should analyze requested languages and themes and then then use /scrips to generate graphs and summaries. The skill should also be able to provide insights about the most viewed articles, trends over time, and comparisons between different topics or languages depending by the request.

 #Overview

 Using /scripts files, skill will analyze data from user input and pass it as the args to the scripts


 #Commands

 When user mentions wikipedia, the skill should analyze requested languages and themes stated in the user input. Then the skill should search for relevant page in wikipedia and then call data_request:get_language_articles() to get the names of articles for all requested languages. Do not waste tokens on searching for names of articles.
 Then call for data_request:fetch_data_page() to get json.
 