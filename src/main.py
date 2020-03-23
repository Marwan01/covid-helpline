# /usr/bin/env python
global DEFAULT_RESPONSE,ADVICE, newsapi, client,bucket, client_twillio

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from google.cloud import storage
from google.cloud.storage import blob

from keys import account_sid, auth_token
from data_utils import *
from responses import *
from news import *
from twillio_utils import *

app = Flask(__name__)



@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    number = request.form['From']
    message_body = request.form['Body']
    save_text(bucket,number,message_body)
    msg_out_response = handle_message(bucket,number,message_body)
    resp = MessagingResponse()
    resp.message('{}'.format(msg_out_response))
    return str(resp)

@app.route("/voice", methods=['GET', 'POST'])
def phone_receiver():
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say(PHONE_MSG, voice='alice')
    # Play an audio file for the caller
    # resp.play('location_pre_recorded_message')

    return str(resp)

client_twillio = Client(account_sid, auth_token)
client = storage.Client(project='covid-helpline')
bucket = client.get_bucket('covid-sms')

if __name__ == "__main__":
    app.run( host='0.0.0.0',port=8080, debug=True)