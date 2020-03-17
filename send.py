# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from datetime import datetime, timedelta
from urllib.error import HTTPError
import numpy as np
from newsapi import NewsApiClient
from google.cloud import storage
from google.cloud.storage import blob
app = Flask(__name__)

global DEFAULT_RESPONSE,ADVICE, newsapi, client,bucket

newsapi = NewsApiClient(api_key='32cbadba12654ed5b8fbf355e5da4ab1')


client = storage.Client(project='covid-helpline')
bucket = client.get_bucket('covid-sms')


DEFAULT_RESPONSE ="""Welcome to the COVID-19 data-line!
Text 'tips' to get information from the CDC about best practices
A location you want the most up to date report. EX: 'Missouri' or 'Italy'
If you want the most up to date news about COVID-19 text: 'News'"""

ADVICE ="""CDC ADVICE: \n
Avoid close contact with people who are sick\n
If you are ill, stay home and seek healthcare if needed\n
Avoid touching your eyes, nose, or mouth with unwashed hands.\n
Cover your coughs or sneezes, in your elbow or into a tissue\n
Wash your hands often with soap and water for at least 20 seconds\n
Clean and disinfect “high touch” objects and surfaces such as doorknobs, faucet handles, railings, and shared keyboards.\n
Get plenty of rest\n
Drink fluids\n
Eating healthy foods\n
Managing your stress may help you prevent getting COVID-19 and recover from it if you do\n
Source: https://www.cdc.gov/coronavirus/2019-ncov/community/"""



def load_csv():
    date = datetime.now().strftime("%m-%d-%Y")
    counter = 1
    while True:
        try:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'
            df = pd.read_csv(url)
            return df
        except HTTPError:
            print("Report wasn't found moving one day back...")
            date = (datetime.now() - timedelta(counter)).strftime("%m-%d-%Y")
            counter += 1



def load_data():
    df = load_csv()
    df['Last Update'] = df['Last Update'].apply(lambda x: x.split("T")[0])
    df = df.replace(np.nan, '', regex=True)
    locations = list(df['Country/Region'].unique()) + list(df['Province/State'].unique())
    return df, locations


def get_data_bas_location(location, df):
    if location.lower() == "US".lower() or  location.lower() == "USA".lower():
        return ["", location, ""] + list(
             df[df['Country/Region'].str.contains(location)].groupby("Country/Region").sum().values[0])
    # elif location == "China"
    # return ["", location, ""] + list(
    #          df[df['Country/Region'].str.contains(location)].groupby("Country/Region").sum().values[0])
    try:
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
    return msg_out




@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    number = request.form['From']
    message_body = request.form['Body']
    save_text(bucket,number,message_body)

    
    msg_out_response = handle_message(message_body)
    resp = MessagingResponse()
    resp.message('{}'.format(msg_out_response))
    return str(resp)

if __name__ == "__main__":
    app.run( host='0.0.0.0',port=8080, debug=True)