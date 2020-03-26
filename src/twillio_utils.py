from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from google.cloud import storage
from google.cloud.storage import blob
from datetime import datetime, timedelta
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from google.cloud import storage
from google.cloud.storage import blob
from datetime import datetime, timedelta
from data_utils import *
from responses import *
from news import return_news
from zip_code import handle_zip_code
import re

import difflib
from keys import account_sid, auth_token
from data_utils import *
from responses import *
from news import *


client_twillio = Client(account_sid, auth_token)


def send_message(msg,number):
    message = client_twillio.messages.create(body=msg,from_='+19142684399',to=number)
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
        try:
            msg = handle_message(bucket,num,loc)
            send_message("New report released for your subscribed location: \n\n"+msg,num)
            suc+=1
        except:
            fail+=1

    return suc,fail

def trigger_daily_sms(bucket):
    sms_to_send = load_data_sms(bucket)
    succes_count, failure_count = send_mass_text(sms_to_send,bucket)

    return f'Sucesfully sent {succes_count} sms. Failed for {failure_count} sms.'

def save_daily_subscription(bucket,phone_number,text):
    location_subscribed = text.split(" ",1)[1]
    path_to_save_subscription = f'sub/{phone_number}/{datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}.txt'
    blob = bucket.blob(path_to_save_subscription)
    blob.upload_from_string(location_subscribed)
    return  f'Thank you. You are now subsribed to daily messages for Corona Virus updates for {location_subscribed}'


def handle_message(bucket,number,message_obj):
    df, locations,states,possible_us = load_data()
    
    
    message = message_obj.rstrip()
    
    #TODO CHECK COUNTRIES BEOFRE US STATES THEN combinned Key
    
    location_clean = difflib.get_close_matches(message, locations,1)
    location_clean_states = difflib.get_close_matches(message, states,1)
    location_clean_us = difflib.get_close_matches(message, possible_us,1)
    location_clean_canada = difflib.get_close_matches(message, ["Canada"],1)

    #CHECK : Advice
    if(message.count("Advice")>0):
        msg_out = ADVICE
    elif(re.search("^[0-9]{5}(?:-[0-9]{4})?$", message)):
        msg_out = handle_zip_code(message,df)
    #CHECK : News
    elif(message.count("News")>0):
        msg_out = return_news()
    #CHECK : Subscribe
    elif(message.count("Subscribe")>0):
        msg_out = save_daily_subscription(bucket,number,message_obj)
    #CHECK : Send all
    elif(message.count("Send all")>0 and number =="+16364749180"):
        msg_out = trigger_daily_sms(bucket)
    #CHECK : for United States
    elif( len(location_clean_us) >0):
        msg_out = handle_message_location("US",df,"Country_Region") 
    #CHECK : Canada
    elif( len(location_clean_canada) >0):
        msg_out = handle_message_location(location_clean_canada[0],df,"Country_Region") 
    #CHECK : USA States 
    elif( len(location_clean_states) >0):
        msg_out = handle_message_location(location_clean_states[0],df,"Province_State") 
    #Countries and cities
    elif( len(location_clean) >0):
        msg_out = handle_message_location(location_clean[0],df,"Combined_Key")
    else:
        msg_out = DEFAULT_RESPONSE
    return msg_out

def save_text(bucket,phone_number,text):
    path_to_save_sms = f'sms/{phone_number}/{datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}.txt'
    blob = bucket.blob(path_to_save_sms)
    blob.upload_from_string(text)
    return True