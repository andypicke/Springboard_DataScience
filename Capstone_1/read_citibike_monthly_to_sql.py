
# Script to read all monthly citibike files to sqlite3 database

# Assumes Monthly csv files already downloaded

# Also assumes empty database has be created. If the table already exists,
# this will add data to it

# Separates data into 2 tables: 'rides' and 'stations', which can be joined on
# w on the station id later if needed

import pandas as pd
import sqlite3
import glob

def clean_citibike_monthly(dat):
    dat.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
    dat.columns = map(str.lower, dat.columns)
    dat.starttime = pd.to_datetime(dat.starttime)
    dat.stoptime  = pd.to_datetime(dat.stoptime)
    dat['gender'] = dat['gender'].astype('category')
    dat['usertype'] = dat['usertype'].astype('category')
    dat['day'] = dat.starttime.dt.day
    dat['month'] = dat.starttime.dt.month
    dat['year']  = dat.starttime.dt.year
    dat['yday']  = dat.starttime.dt.dayofyear
    dat['wkday'] = dat.starttime.dt.dayofweek
    dat['hour']  = dat.starttime.dt.hour
    return dat

flist = glob.glob('data/historical/*data.csv')
#flist

## Make sure database is empty before running this (otherwise will append on)

non_station_vars = ['tripduration','starttime','stoptime','start_station_id','end_station_id','bikeid','usertype','birth_year','gender','day','month','year','yday','wkday','hour']
sta_start_vars = ['start_station_id','start_station_name','start_station_latitude','start_station_longitude']
sta_end_vars = ['end_station_id','end_station_name','end_station_latitude','end_station_longitude']

con = sqlite3.connect("data/citibike_database.db3")

for fname in flist:
    print('wokring on ' + fname)

    reader = pd.read_csv(fname,parse_dates=True,chunksize=100000)

    for chunk in reader:
        print('reading chunk')

        # some names change starting 2016/10 ; make them same as previous names
        if any(chunk.columns.isin(['Trip Duration'])):
            chunk.rename(columns={'Trip Duration':'tripduration'},inplace=True)
        if any(chunk.columns.isin(['Start Time'])):
            chunk.rename(columns={'Start Time':'starttime'},inplace=True)
        if any(chunk.columns.isin(['Stop Time'])):
            chunk.rename(columns={'Stop Time':'stoptime'},inplace=True)
        if any(chunk.columns.isin(['Bike ID'])):
            chunk.rename(columns={'Bike ID':'bikeid'},inplace=True)
        if any(chunk.columns.isin(['User Type'])):
            chunk.rename(columns={'User Type':'usertype'},inplace=True)


        dat = clean_citibike_monthly(chunk)
        dat2 = dat[non_station_vars]
        #print('adding ' + fname + ' to sql database')
        dat2.to_sql("rides",con,if_exists='append',index=False)
        del dat2
        df_start = dat[sta_start_vars]
        df_end = dat[sta_end_vars]
        del chunk
        del dat
        df_start.columns = ['id','name','lat','lon']
        df_end.columns = ['id','name','lat','lon']
        df_comb = pd.concat([df_start,df_end])
        del df_start
        del df_end
        df_comb.drop_duplicates(inplace=True)
        df_comb.to_sql("stations",con,if_exists='append',index=False)
        del df_comb

    del reader

print('done reading data')

print('making stations table distinct')
# Get distinct rows from 'stations' table and make new table with just those (replace existing table)
stations_dist = pd.read_sql_query("SELECT DISTINCT * FROM stations",con)
stations_dist.to_sql("stations",con,if_exists='replace',index=False)

con.close()
