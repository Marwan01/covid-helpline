# /usr/bin/env python

global DEFAULT_RESPONSE,ADVICE, newsapi, client,bucket, client_twillio

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from google.cloud import storage
from google.cloud.storage import blob

from keys import account_sid, auth_token
from data_utils import *
from news import *
from responses import *


def handle_message(bucket,number,message_obj):
    df, locations = load_data()
    message = message_obj.rstrip()
    if(message.count("Advice")>0):
        msg_out = ADVICE
    elif(message.count("News")>0):
        msg_out = return_news()
    elif(message.count("Subscribe")>0):
        msg_out = save_daily_subscription(bucket,number,message_obj)
    elif(message.count("Send all")>0 and number =="+16364749180"):
        msg_out = trigger_daily_sms(bucket)
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
    msg_out_response = handle_message(bucket,number,message_body)
    resp = MessagingResponse()
    resp.message('{}'.format(msg_out_response))
    return str(resp)

app = Flask(__name__)
client_twillio = Client(account_sid, auth_token)
client = storage.Client(project='covid-helpline')
bucket = client.get_bucket('covid-sms')

if __name__ == "__main__":
    app.run( host='0.0.0.0',port=8080, debug=True)
