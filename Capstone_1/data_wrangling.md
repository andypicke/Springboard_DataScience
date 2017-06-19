
## Data Wrangling description for Citibike Analysis

- Describe the data wrangling steps that you undertook to clean your capstone project data set.
- What kind of cleaning steps did you perform? How did you deal with missing values, if any?
- Were there outliers, and how did you decide to handle them?

This document will eventually become part of your milestone report.


## Historical citibike data

Historical usage data is made available in csv format by Citibike at <>. Each file contains one month of data, and data is available (as of xx) from xx to xx. Each data file contains the following fields:

-Trip Duration (seconds)
- Start Time and Date
- Stop Time and Date
- Start Station Name
- End Station Name
- Station ID
- Station Lat/Long
- Bike ID
- User Type (Customer = 24-hour pass or 7-day pass user; Subscriber = Annual Member)
- Gender (Zero=unknown; 1=male; 2=female)
- Year of Birth

This data has been processed to remove trips that are taken by staff as they service and inspect the system, trips that are taken to/from any of our “test” stations (which we were using more in June and July 2013), and any trips that were below 60 seconds in length (potentially false starts or users trying to re-dock a bike to ensure it's secure).

Data files is downloaded w/ the script xx.py

The data is cleaned and modified, and saved to a SQLite3 database in the script read_citibike_to_sql.ipynb

Cleaning/modifications:

- Spaces in variable names are replaced w/ underscores
- gender and usertype variables are converted to cateogry type
- starttime and stoptime variables are converted to datetime
- New variables day, month, year, yday, wkday, hour are added

Station-related variables (except id) are not saved with ride data .A separate table is made with info for unique stations.




## Weather data


Historical weather data for LaGuardia airport was downloaded from <https://www.wunderground.com/> and saved to a SQLite3 database.

Cleaning:
- bad values/outliers?
- reduce # fields kept
- rename variables
- add fields yday, year, month?



## Holidays

Data on US holidays was collected from ??, since I expect holidays to have a significant effect on Citibike usage.


## Streaming citibike data

Citibike also makes available streaming data on system status at <https://gbfs.citibikenyc.com/gbfs/en/station_status.json>. A script (read_citibike_streaming.py) was written to read this data, and a chron-job was set up to retrieve data every half hour. Data was saved to a sqlite3 database, and csv files were also saved locally.