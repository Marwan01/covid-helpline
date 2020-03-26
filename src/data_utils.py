from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from responses import *
import re
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

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
    states = list(set(list(df['Province_State'].dropna())))[1:]
    possible_us = ['Us','United States',"USA","United States of America","Usa"]

    return df, locations, states,possible_us

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
    message = f'In {row[0]}:\n' \
              f'Confirmed:{int(row[1])} (+{int(row[4])} from yesterday), \n' \
              f'Recovered:{int(row[2])} (+{int(row[5])} from yesterday), \n' \
              f'Deaths:{int(row[3])} (+{int(row[6])} from yesterday), \n' \
              f'as of {datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")}. ' 
    message = message.replace("  ", " ")
    return message

def handle_message_location(location,df,key):
    row = clean_df_row(df,key,location)
    date = df['Last Update'].iloc[0]
    msg_out = generate_message_from_row_v2(row,date)
    return msg_out

def load_data_sms(bucket):
    data = {}
    for b in bucket.list_blobs(prefix='sub/'):
        blob_path = b.name
        b1 = blob_path[blob_path.find("+1")+2:blob_path.rfind("/")]
        data[b1] = b.download_as_string().decode('utf-8')
    return data
