# Capstone Project 1 Proposal : Analysis of Bike-share data from NYC.
 
Andy Pickering
 
## 1. What is the problem you want to solve? 
 
- Predict demand (number of rides taken) for NYC citi-bike system, based on variables such as weather, day of week, hour, etc.. 
 
- Predict availability of bikes at stations.
 
- Identify which factors influence demand the most.
 
## 2. Who is your client and why do they care about this problem? In other words, what will your client DO or DECIDE based on your analysis that they wouldn’t have otherwise? 
 
- The potential client could be the bike-share program, which needs to plan ahead and make sure there are enough bikes to meet the demand. Other city transportation agencies could be interested as well ; for example if fewer people bike on bad weather days, they may take the bus or train instead, and demand for those would increase.
 
## 3. What data are you going to use for this? How will you acquire this data? 
 
- Monthly citi-bike data files are available at https://www.citibikenyc.com/system-data and  :https://s3.amazonaws.com/tripdata/index.html . I have read one file into pandas, and the data seems relatively clean, making it suitable for this first project.
 
- Daily weather data can be downloaded from weather underground (I have done this previously). I will also investigate other sources of historical weather data.
 
## 4. In brief, outline your approach to solving this problem (knowing that this might change later). 
 
- Download citi-bike data for at least one year (to get full seasonal cycle of weather)
- Each monthly file is on the order of 200MB, which can be easily read and analyzed with pandas for example
- However, combining all years may be too large to handle in memory at once. 
- Could read in one file at a time, condense data into daily/hourly aggregates, and save smaller csv files.
- Could read all data into a sql database, then query that for future analysis. This would also give me experience populating and querying a sql database.
- Aggregate data by month, day, and hour to examine patterns of usage.
- Examine relationship between the number of rides and weather (scatter plots, correlation etc.).
- Split data into training/testing sets, build model (multiple linear regression, random forest, etc)  to predict number of rides based on weather and other variables, and quantify its performance . 
 
I would also like to analyze other transportation data (bus, Uber, train etc.) to see if changes in bike usage are compensated by changes in usage on those systems. However, this is likely beyond the scope of this first capstone project.
 
## 5. What are your deliverables? Typically, this would include code, along with a paper and/or a slide deck.
 
- Clear, documented code that will reproduce the entire analysis, and show what steps were taken in the analysis. Likely in a jupyter notebook format. Longer code could be provided separately and referenced in notebook.
- A slide deck presenting the results and implications of the analysis to the client.
- All deliverables will be in a github repository.
