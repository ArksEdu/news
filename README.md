# News Report
This project returns the answers to the following 3 questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The main code file is newsreport.py.   This file is dependent on the following libraries:
- psycopg2
- bleach

The newsreport.py file has 3 primary functions - one to answer each question:
- get_topArticles - this returns the top 3 articles that have been viewed the most
- get_topAuthors - this returns the authors in order of popularity
- get_errorPercentages - this returns the days on which more than 1% of views resulted in an error

To generate the output follow these directions:
- download newsdata.zip file from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- extract the newsdata.sql file from the zip file
- copy the downloaded newsdata.sql file into the same folder as the newsreport.py file
- navigate to this folder in Vagrant through ssh
- use the command "psql -d news -f newsdata.sql" to set up the data
- use the command "python newsreport.py" to run this project and generate output

The output of the newsreport.py is available in the newsreportOutput.txt file.  This output is based on the data in the newsdata.sql file provided by Udacity.
