from google.cloud import storage
from google.cloud.storage import blob
from twilio.rest import Client
import re
import numpy as np
import pandas as pd
import us
from datetime import datetime, timedelta
from math import cos, asin, sqrt
from uszipcode import SearchEngine
import difflib
from keys import account_sid, auth_token, news_api_key

client = storage.Client(project='covid-helpline')
bucket = client.get_bucket('covid-sms')
today_date = datetime.now().strftime("%m-%d-%Y")
DEFAULT_RESPONSE ="""Welcome to the Covid-19 Helpline. \n
- Text 'Advice' to get information on how to protect yourself from Covid-19.\n
- Text 'News' to get the most popular daily news article about Covid-19.\n
- Text your country, state, city name, or zip code to get the latest available report on Covid-19 in your area.\n
- Text 'Subscribe' followed by country/state name to receive the most up to date Covid-19 count report from John Hopkins as soon as it is released.\n
- Text 'Initiative' to learn more about our work and our mission to fight coronavirus.\n
- Text 'Stop' to opt out."""


def handle_message(message_obj):
    df, locations,states,possible_us, countries = load_data()
    
    
    message = message_obj.rstrip()
    print(message_obj)
    

    location_clean = difflib.get_close_matches(message, locations,1,0.65)
    location_clean_country = difflib.get_close_matches(message, countries,1,0.8)

    location_clean_states = difflib.get_close_matches(message, states,1,0.8)
    location_clean_us = difflib.get_close_matches(message, possible_us,1)
    location_clean_canada = difflib.get_close_matches(message, ["Canada"],1)

    #CHECK : Advice
    if(message.count("Advice")>0):
        msg_out = ADVICE
    elif(re.search("^[0-9]{5}(?:-[0-9]{4})?$", message)):
        msg_out = handle_zip_code(message,df)
    elif( len(location_clean_us) >0):
        msg_out = handle_message_location("US",df,"Country_Region") 
    #CHECK : Canada
    elif( len(location_clean_canada) >0):
        msg_out = handle_message_location(location_clean_canada[0],df,"Country_Region") 
    #CHECK: Counntries
    elif( len(location_clean_country) >0):
        msg_out = handle_message_location(location_clean_country[0],df,"Country_Region") 
    #CHECK : USA States 
    elif( len(location_clean_states) >0):
        msg_out = handle_message_location(location_clean_states[0],df,"Province_State") 
    #Countries and cities
    elif( len(location_clean) >0):
        msg_out = handle_message_location(location_clean[0],df,"Combined_Key")
    else:
        msg_out = DEFAULT_RESPONSE
    return msg_out

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
    try:          
        search = SearchEngine(simple_zipcode=True)
        zipcode = search.by_zipcode(code)
        data_lat_long=load_lat_long_data(df)
        v = {'lat': zipcode.lat, 'lon': zipcode.lng}
        lat,long = closest(data_lat_long, v)
        location_cleaned_after_zip = filter_df_lat_long(df,lat,long)
        msg_out = handle_message_location(location_cleaned_after_zip,df,'Combined_Key')#MATACHES UP KEY @@!!
    except:
        msg_out = "Zip code not found"
    return msg_out


def load_csv():
    date = datetime.now().strftime("%m-%d-%Y")
    counter = 1
    df = None
    while df is None:
        try:
            date_yesterday = (datetime.strptime(date, "%m-%d-%Y")- timedelta(1)).strftime("%m-%d-%Y")
            url_yesterday = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date_yesterday}.csv'
            df_yest = pd.read_csv(url_yesterday)
            url_today = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'
            df_today = pd.read_csv(url_today)
            df = pd.merge(df_today,df_yest, on = 'Combined_Key', suffixes = ("","_yesterday"))

            return df
        except:
            print("Report wasn't found moving one day back...")
            print(date)
            date = (datetime.now() - timedelta(counter)).strftime("%m-%d-%Y")
            counter += 1


def load_data():
    df = load_csv()
    df['Last Update']=df['Last_Update'].apply( lambda text : re.search(r'\d{4}-\d{2}-\d{2}', text).group())
    df = df.replace(np.nan, '', regex=True)
    locations = list(df['Combined_Key'].unique())
    df['Long_'] = pd.to_numeric(df['Long_'])
    df['Lat'] = pd.to_numeric(df['Lat'])
    states = list(set(list(df['Province_State'].dropna())))[1:]
    possible_us = ['Us','United States',"USA","United States of America","Usa"]
    countries = list(df['Country_Region'].unique())    
    
    return df, locations, states, possible_us, countries


def clean_df_row(df, key,search_value):
    grouped = df.groupby(key).sum().reset_index()
    grouped.columns.values[0]='Location'
    location = grouped[grouped['Location']==search_value]['Location'].values[0]
    
    Confirmed = grouped[grouped['Location']==search_value]['Confirmed'].values[0]
    Confirmed_yesterday = grouped[grouped['Location']==search_value]['Confirmed_yesterday'].values[0]
    new_confirmed = Confirmed -Confirmed_yesterday
    
    Deaths = grouped[grouped['Location']==search_value]['Deaths'].values[0]
    Deaths_yesterday = grouped[grouped['Location']==search_value]['Deaths_yesterday'].values[0]
    new_deaths = Deaths-Deaths_yesterday

    
    Recovered = grouped[grouped['Location']==search_value]['Recovered'].values[0]
    Recovered_yesterday = grouped[grouped['Location']==search_value]['Recovered_yesterday'].values[0]
    new_recovered = Recovered-Recovered_yesterday
    return [location,Confirmed,Recovered,Deaths,new_confirmed,new_recovered,new_deaths]

def generate_message_from_row_v2(row,date):

    location,Confirmed,Recovered,Deaths,new_confirmed,new_recovered,new_deaths = row

    if Recovered == 0 : 
        _Recovered = 1 
    else: 
        _Recovered = Recovered
    if Confirmed == 0 : 
        _Confirmed = 1 
    else: 
        _Confirmed = Confirmed
    if Deaths == 0 : 
        _Deaths = 1 
    else: 
        _Deaths = Deaths
        
    growt_rate_recovered = int(new_recovered/_Recovered*100)
    growt_rate_confirmed = int(new_confirmed/_Confirmed*100)
    growt_rate_deaths = int(new_deaths/_Deaths*100)


    message = f'In {row[0]} on {datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")}:\n' \
              f'Confirmed cases: {int(row[1])}\n+{new_confirmed} from yesterday, growth rate: +{growt_rate_confirmed}%' \
              f'\nRecovered cases: {int(row[2])}\n+{new_recovered} from yesterday.' \
              f'\nDeaths: {int(row[3])}\n+{new_deaths} from yesterday.' 
    message = message.replace("  ", " ")
    return message

def handle_message_location(location,df,key):
    row = clean_df_row(df,key,location)
    date = df['Last Update'].iloc[0]
    msg_out = generate_message_from_row_v2(row,date)
    return msg_out


def send_message(msg,number):
    message = client_twillio.messages.create(body=msg,from_='+19142684399',to=number)
    print(f"send to {number}")
    return message.sid
def load_data_sms(bucket):
    data = {}
    for b in bucket.list_blobs(prefix='sub/'):
        blob_path = b.name
        b1 = blob_path[blob_path.find("+1")+2:blob_path.rfind("/")]
        data[b1] = b.download_as_string().decode('utf-8')
    return data

def send_mass_text(data,bucket):
    suc= 0
    fail = 0
    for num, loc in data.items():
        if check_location(loc):
            try:
                msg = handle_message(loc)
                send_message("New report released for your subscribed location: \n\n"+msg,num)
                print(loc,num)
                suc+=1
            except:
                fail+=1
        else:
            fail+=1


    return suc,fail


def trigger_daily_sms(bucket):
    sms_to_send = load_data_sms(bucket)
    succes_count, failure_count = send_mass_text(sms_to_send,bucket)
    msg = f'Sucesfully sent {succes_count} sms. Failed for {failure_count} sms.'
    send_message(msg,"+16364749180")

    return msg

def check_locations(locations):
    if len(locations)>0:
        return True
    else:
        return False
    
def check_location(location):
    df, locations,states,possible_us, countries = load_data()
    
    result = handle_zip_code(location,df)
    
    
    message = location.rstrip()
    print(location)
    

    location_clean = difflib.get_close_matches(message, locations,1,0.65)
    if check_locations(location_clean): return True
    print(location_clean)
    
    location_clean_country = difflib.get_close_matches(message, countries,1,0.8)
    if check_locations(location_clean_country): return True

    location_clean_states = difflib.get_close_matches(message, states,1,0.8)
    if check_locations(location_clean_states): return True
    
    location_clean_us = difflib.get_close_matches(message, possible_us,1)
    if check_locations(location_clean_us): return True
    print(location_clean_us)
    
    location_clean_canada = difflib.get_close_matches(message, ["Canada"],1)
    if check_locations(location_clean_canada): return True
    
    return result


trigger_daily_sms(bucket)
