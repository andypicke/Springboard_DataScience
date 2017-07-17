# This script downloads daily historical weather data from wunderground,
# for citibike analysis project.

# Saves a modified file to sqlite3 database

import sqlite3
import pandas as pd

def get_wea_data_yearly(year,station):
    """
    Get historical (daily) weather data from wunderground for specified year and station
    """
    url = 'http://www.wunderground.com/history/airport/' + station + '/' + year + '/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=' + year + '&req_city=NA&req_state=NA&req_statename=NA&format=1'
    dat = pd.read_csv(url,parse_dates=True)
    # Name of date column is tz, which varies so we can't hardwire name
    dat.iloc[:,0] =  pd.to_datetime(dat.iloc[:,0])
    dat['date'] = dat.iloc[:,0]
    dat.set_index(dat.date, inplace=True)
    dat['yday'] = dat.date.dt.dayofyear
    dat['month'] = dat.date.dt.month
    dat['year'] = dat.date.dt.year
    dat.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
    dat['st_code'] = station
    vars_to_keep = ['date','st_code','Max_TemperatureF','Min_TemperatureF','Mean_TemperatureF','year','yday','month','PrecipitationIn','_CloudCover','_Max_Gust_SpeedMPH','_Events']
    dat = dat[vars_to_keep]
    dat.rename(columns={'Max_TemperatureF':'max_temp','Min_TemperatureF':'min_temp','Mean_TemperatureF':'mean_temp','PrecipitationIn':'precip_In','_CloudCover':
        'cloud_cover','_Max_Gust_SpeedMPH':'max_gust_mph','_Events':'events'},inplace=True)

    return dat

# Write to databse
con = sqlite3.connect("data/nyc_weather.db3")

years = ['2013','2014','2015','2016','2017']
# KGLA is code for LaGuardia airport
for year in years:
    dat = get_wea_data_yearly(year,'KLGA')
    dat.to_sql("temps",con,if_exists='append',index=False)
    del dat
