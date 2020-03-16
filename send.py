
import pandas as pd 
from datetime import datetime, timedelta
import numpy as np
import pickle, json

url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-11-2020.csv'
df = pd.read_csv(url)
df['Last Update'] = df['Last Update'].apply(lambda x: x.split("T")[0])
df = df.replace(np.nan, '', regex=True)
LOCATIONS = list(df['Country/Region'].unique()) + list(df['Province/State'].unique())

def get_data_bas_location(location):
    if (location == "US" or location == "China"):
        return ["",location,""] + list(df[df['Country/Region'].str.contains(location)].groupby("Country/Region").sum().values[0])
    try:  
        dd = df[df['Country/Region'].str.contains(location)].values[0]
    except:
        dd = df[df['Province/State'].str.contains(location)].values[0]
    return list(dd)


def generate_message_from_row(row):
    message = f'As of {datetime.now().strftime("%B %d, %Y")}  In {row[0]} {row[1]} there are currenty \n'\
    f'{row[3]} confirmed, \n'\
    f'{row[5]} Recovered \n'\
    f'and {row[4]} Deaths'
    message = message.replace("  "," ")
    return message


def handle_message(message_obj):
    check_new_data(message_obj)
 
    message = message_obj.body.rstrip()
    if(message.count("Tips")>0):
        msg_out = return_tips()
    elif(message.count("Daily")>0):
        msg_out = subscribe_daily(message_obj)
    elif( message in LOCATIONS):
        row_test = get_data_bas_location(message)
        msg_out = generate_message_from_row(row_test)
    else:
        msg_out = DEFAULT_RESPONSE
    send_text(msg_out,message_obj.from_number)


    #### just a test change to check branch
