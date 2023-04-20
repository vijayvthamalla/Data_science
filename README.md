# Data_science
**Data Science projects (Complete end to end steps required to perform a data science project)**
There were three projects added in this repository. These three projects will help in exposure to different basics of data science field such as

**1) Data gathering or collecting using web scraping:**
This is the first task in any Data science project, collecting the data can be a costliest task on hand as the data we are looking for might not be available in the same format as expected or some of the data can be irrevelant and some of the data we need could be missing. We can collect the data in different ways, one of the popular method is web scraping. Web scraping allows us to collect the data that is freely available in internet without much hassle of manual intervention.

File *web_scraping_national_parks.py* shows us a sample of code on how to collect the data on internet using web scraping libraries beautifulsoup and requests.

**2) Data wrangling or Data cleaning or Data preprocessing:**
In this task we will take the data and conduct study or initial analysis of the data. Pandas library is very useful in performing data analysis or modifications as it allows us to use data in a powerful format called Dataframes. Dataframes present the data in a nice tabular format like sql tables. They were easy to interpret and pandas took it to next level by allowing powerful modifications on the dataframes without the hassle of using different libraries for different functions.

File *data_wrangling_board_games* shows how pandas can be used for modifying the data as we need, there are hundreds of more functionalities as needed. Pandas documentation at https://pandas.pydata.org/docs/ is a good starting point to learn more about pandas.

**3)applying Machine learning methodologies:**
There are various types of machine learning tasks at hand such as classification, regression, clustering, dimensionality reduction, etc.
Here we focussed on Classification using a heavily adjusted dataset on Data science workers and learners. You can see an overview of how we added the data into a pandas dataframe and then performed data cleaning and preprocessing. Finally we utilized 3 of the classification algorithms such as Decision Tree classifier, Logistic Regression (although the name contains regression in it, it is actually a classification algorithm), K-Neighbors Classifier. Selection of an algorithm for a task at hand involves a lot of assumptions taken carefully analyzing the data or you can experiment with different algorithms

File *Data_science_workers_classification.ipynb* provides a sample code of classification task.
