# sqlalchemy-challenge
sqlalchemy-challenge Assignment - Milinda 'ML' Liyanage

## Summary

* This assignment is in two sections.
* First section is done through a jupyter notebook to analyse the data.
* Second section is using Flask to display the data on a web browser.
* There are a couple of bonus sections, which has been attempted but not fully completed.

### The following steps were done for the first section, precipitation & station analysis: 

* Started from the jupyter notebook provided. [climate](climate.ipynb)
* Created a connection to the SQLite database.
* Identified the tables and their columns in database.
* Read the data and answered the questions in the assignment about precipitation & weather stations.
* Created a bar chart for precipitation and saved it. [Precipitation by Date](Images/Precipitation_by_Date_bar.png)
* A histogram was created and saved for the most active weather station. [Active Weather Station](Images/Active_Station_Observations_hist.png) 

### The following steps were done for the second section, creating an app: 

* A new python file called [app](app.py) created. 
* As required five routes were created for application.
* Using the code that was created in the first section, functions were created for each route.
* The return values from the functions were jsonified so the results could be displayed on the web browser.

## Bonus section

### Temperature Analysis I

#### Modified the starter [temp_analysis_bonus_1](temp_analysis_bonus_1.ipynb) file and did the following;
* After reading the measurement data the date string column was converted to date type column.
* Then the date was set as the index.
* Added a new column day, and the date column was dropped.
* Two new data frames were created for June and December temperature observations, 30 days per month.
* Mean temperature for both data sets were identified.
* Create two average value data set, grouping by day.
* Using the two grouped data sets, ran a paired t-test.
* Results of the t-test had pvalue of 6.06 e-16.

#### Analysis
* The null hypotheses: the true mean difference is equal to zero for June and December temperature observations.
* Alternative hypotheses: the true mean difference is not equal to zero.

* As the p-value is very small the null hypothesis cannot be supported. Therefore, there is a difference between June and December temperature observations.

### Temperature Analysis II

* not attempted
