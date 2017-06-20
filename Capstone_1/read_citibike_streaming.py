#!/usr/bin/env python

# To Add:
# - write data to S3 bucket
# - Write a log file



# import libraries
import requests
import pandas as pd
import sqlite3

# url for data on station status:
station_url = 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json'

# get json from API
r = requests.get(station_url)
dat = r.json() # returns dictionary

# make dataframe of station data
df=pd.DataFrame( dat['data']['stations'] )

# write raw data to csv so we can always go back later if needed
csv_name = '/Users/Andy/Springboard_DataScience/Capstone_1/data/feeds/' + str(pd.to_datetime(dat['last_updated'],unit='s')) + '.csv'
df.to_csv(csv_name,index=False)

# add timestamp to rows (this is in UTC)
#timestamp_utc = pd.to_datetime(dat['last_updated'],unit='s', utc=True )
timestamp_utc = pd.to_datetime(dat['last_updated'],unit='s',utc=True)
df['timestamp_utc'] = timestamp_utc.to_datetime64()
#df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'] )

# also add local (NYC) time
timestamp_nyc = timestamp_utc.tz_convert(tz='America/New_York')
df['timestamp_nyc'] = timestamp_nyc.to_datetime64()
#df['timestamp_nyc'] = pd.to_datetime(df['timestamp_nyc'])

# add yearh, hour, day of year (using NY time)
df['year']=df.timestamp_nyc.dt.year
df['hour']=df.timestamp_nyc.dt.hour
df['yday']=df.timestamp_nyc.dt.dayofyear

# write the data to sql database
con = sqlite3.connect("/Users/Andy/Springboard_DataScience/Capstone_1/data/citibike_feeds.db3")
df.to_sql("station_status",con,if_exists='append',index=False)
con.close()
