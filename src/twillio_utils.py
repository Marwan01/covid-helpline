from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from google.cloud import storage
from google.cloud.storage import blob
from datetime import datetime, timedelta
from .data_utils import *
from .responses import *
from .news import return_news


def send_message(msg,number):
    # Where do you get client_twillio???
    message = client_twillio.messages.create(body=msg,from_='+19142684399',to=number)
    return message.sid


def load_data_sms(bucket):
    data = {}
    for b in bucket.list_blobs(prefix='sub/'):
        blob_path = b.name
        b1 = blob_path[blob_path.find("+1")+2:blob_path.rfind("/")]
        data[b1] = b.download_as_string().decode('utf-8')
    return data


def send_mass_text(data):
    suc= 0
    fail = 0
    for num, loc in data.items():
        try:
            # where do you get bucket???
            msg = handle_message(bucket,num,loc)
            send_message("New report released for your subscribed location: \n\n"+msg,num)
            suc+=1
        except:
            fail+=1
    return suc,fail


def trigger_daily_sms(bucket):
    sms_to_send = load_data_sms(bucket)
    succes_count, failure_count = send_mass_text(sms_to_send)

    return f'Sucesfully sent {succes_count} sms. Failed for {failure_count} sms.'


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


def save_text(bucket,phone_number,text):
    path_to_save_sms = f'sms/{phone_number}/{datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}.txt'
    bucket.blob(path_to_save_sms).upload_from_string(text)
    return True


def save_daily_subscription(bucket,number,message_obj):
    # TODO what should be a path to save subscriptions?
    path_to_subscription = f'sms/...'
    bucket.blob(path_to_subscription).upload_from_string(message_obj)
    return True
