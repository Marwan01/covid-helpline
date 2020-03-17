# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from datetime import datetime, timedelta
from urllib.error import HTTPError
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
    except:
        dd = df[df['Country/Region'].str.contains(location)].values[0]
    return list(dd)


def generate_message_from_row(row):
    message = f'As of {datetime.now().strftime("%B %d, %Y")}  In {row[0]} {row[1]} there are currenty \n' \
              f'{row[3]} confirmed, \n' \
              f'{row[5]} Recovered \n' \
              f'and {row[4]} Deaths'
    message = message.replace("  ", " ")
    return message


def handle_message_location(location,df):


    row = get_data_bas_location(location, df)
    msg_out = generate_message_from_row(row)
    return msg_out



def return_news():
    top_headlines = newsapi.get_top_headlines(q='corona virus',
                                          category='health',
                                          language='en',
                                          country='us')
    NEWS  ="Top headlines from today about Covid-19 cases are: "

    for el in top_headlines['articles'][:5]:
        NEWS += "--"+ el['title'] + '\n'
    NEWS
    return NEWS


def save_text(bucket,phone_number,text):
    path_to_save_sms = f'sms/{phone_number}/{datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}.txt'
    blob = bucket.blob(path_to_save_sms)
    blob.upload_from_string(text)
    return True


def save_daily_subscription(bucket,phone_number,text):
    location_subscribed = text.split(" ",1)[1]
    path_to_save_subscription = f'sub/{phone_number}/{datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}.txt'
    blob = bucket.blob(path_to_save_subscription)
    blob.upload_from_string(location_subscribed)
    return  f'Thank you. You are now subsribed to daily messages for Corona Virus updates for {location_subscribed}'



def handle_message(message_obj):

    df, locations = load_data()
    message = message_obj.rstrip()
    if(message.count("Tips")>0):
        msg_out = ADVICE
    elif(message.count("News")>0):
        msg_out = return_news()
    elif(message.count("Subscribe")>0):
        msg_out = subscribe_daily(message_obj)
    elif( message in locations):
        msg_out = handle_message_location(message,df)
    else:
        msg_out = DEFAULT_RESPONSE
    send_text(msg_out,message_obj.from_number)


    #### just a test change to check branch
