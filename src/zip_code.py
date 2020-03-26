## US DOCUMENTATION: https://pypi.org/project/us/
import us
## USZIPCODE DOCUMENTATION: https://pypi.org/project/uszipcode/
from datetime import datetime, timedelta
from math import cos, asin, sqrt
from uszipcode import SearchEngine
from data_utils import load_csv, handle_message_location

import pandas as pd 

today_date = datetime.now().strftime("%m-%d-%Y")


def load_lat_long_data(df):
    d = list(zip(df['Lat'].values,df['Long_'].values))
    data_lat_long = [{"lat": lat, "lon": lon} for lat, lon in d]
    return data_lat_long

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, v):
    minval = min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))
    return minval['lat'],minval['lon']

def filter_df_lat_long(df,lat,long):
    return df[(df['Lat']==lat) & (df['Long_']==long )]['Combined_Key'].values[0]#MATACHES LOW KEY @@!!


def handle_zip_code(code,df):            
    search = SearchEngine(simple_zipcode=True)
    zipcode = search.by_zipcode(code)
    data_lat_long=load_lat_long_data(df)
    v = {'lat': zipcode.lat, 'lon': zipcode.lng}
    lat,long = closest(data_lat_long, v)
    location_cleaned_after_zip = filter_df_lat_long(df,lat,long)
    print(location_cleaned_after_zip)
    msg_out = handle_message_location(location_cleaned_after_zip,df,'Combined_Key')#MATACHES UP KEY @@!!
    return msg_out