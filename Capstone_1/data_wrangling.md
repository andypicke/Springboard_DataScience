
# Data Wrangling description for Citibike Analysis


## Historical citibike data

Historical usage data is made available in csv format by Citibike at <https://s3.amazonaws.com/tripdata/index.html>. Each file contains one month of data, and data is available (as of June 19, 2017) from July 2013 to March 2017. Each data file contains the following fields (description is from Citibike website):

- Trip Duration (seconds)
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

Since the data are stored in a public Amazon S3 bucket, all the monthly files can be downloaded w/ the following command at the terminal:
```
aws s3 cp s3://tripdata . --recursive --exclude "*JC"
```

You can then unzip all files and remove zip files w/:
```
unzip \*.zip
rm *.zip
```

The total amount of data is too large to work with in memory, so a SQL database is used. The data in CSV files is cleaned, modified, and saved to a SQLite3 database in the script _read_citibike_to_sql.ipynb_ . The complete database is approximately 3.7GB in size and contains over 39 million rows (rides). The data is farily clean to begin with, but some steps are taken.

Cleaning/modifications:

- Spaces in variable names are replaced w/ underscores
- _gender_ and _usertype_ variables are converted to cateogry type
- _starttime_ and _stoptime_ variables are converted to datetime
- New variables _day_, _month_, _year_, _yday_, _wkday_, and _hour_ are computed from _starttime_ and added to enable easy sorting and grouping.

Station-related variables except _id_ (name, lat,long ) are not saved in the table with ride data, in order to reduce the size. A separate table 'stations' is made with the info for unique stations, which can be joined to the 'rides' table using the station ID key if needed.

Upon examining the rider age distribution, there appear to be a small number of incorrect values or typos. A very small fraction of riders have ages over 100, up to 159!. Since the [oldest living person](https://en.wikipedia.org/wiki/List_of_the_verified_oldest_people) is 116 it seems likely that these are mistakes in the data. Birth year, not age, was recorded, so my best guess is that 18 was intered instead of 19 for the beginning of some years (ie 1895 instead of 1995). These age values will be converted to NaN in the dataset.


## Weather data

Historical weather data for LaGuardia airport is downloaded from <https://www.wunderground.com/> and saved to a SQLite3 database with the script **get_weather_data.py**

Cleaning/ Modifications:
- Data is converted to datetime and set as index
- Spaces in variable names replaced with underscores
- Add fields yday, year, month
- Keep only temperature weather fields


## Holidays

Data on US holidays will be collected from <https://holidayapi.com/>, since I expect holidays to have a significant effect on Citibike usage.


## Streaming citibike data

Citibike also makes available streaming data on system status at <https://gbfs.citibikenyc.com/gbfs/en/station_status.json>. A script (_read_citibike_streaming.py_) was written to read this data, and a chron-job was set up to retrieve data every 15 min. Data is saved to a sqlite3 database, and csv files are also saved locally.
