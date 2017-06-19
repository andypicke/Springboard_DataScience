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

# add timestamp to rows
df['timestamp']=pd.to_datetime(dat['last_updated'],unit='s')

df['year']=df.timestamp.dt.year
df['hour']=df.timestamp.dt.hour
df['yday']=df.timestamp.dt.dayofyear

# write the data to sql database
con = sqlite3.connect("/Users/Andy/Springboard_DataScience/Capstone_1/data/citibike_feeds.db3")
df.to_sql("station_status",con,if_exists='append',index=False)
con.close()

# write to csv also
csv_name = '/Users/Andy/Springboard_DataScience/Capstone_1/data/feeds/' + str(pd.to_datetime(dat['last_updated'],unit='s')) + '.csv'
df.to_csv(csv_name,index=False)
