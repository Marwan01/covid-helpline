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

    # Sends verification text... seems to work with rate limiting set, must see if implementation allows using this to MessagingResponse() instead. Contacting Twilio support
    verification = client_twillio.verify \
                     .services(limit_service.sid) \
                     .verifications \
                     .create(rate_limits={
                          'end_user_phone_number': '##########' # Sparse documentation for this, contacted support to get more info
                      }, to=number, channel='sms')


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

# Google Cloud client
client = storage.Client(project='covid-helpline')
bucket = client.get_bucket('covid-sms')


# Verification Service prerequisite for rate limiting
limit_service = client_twillio.verify.services.create(friendly_name='Rate Limit Service')

rate_limit = client_twillio.verify \
    .services(limit_service.sid) \
    .rate_limits \
    .create(
         description='Limit verifications by Phone Number',
         unique_name='end_user_phone_number'
     )


limit_bucket = client_twillio.verify.services(limit_service.sid) \
                      .rate_limits(rate_limit.sid) \
                      .buckets \
                      .create(max=10, interval=14440)   # Cap at 10 requests per 4 hours




if __name__ == "__main__":
    app.run( host='0.0.0.0',port=8080, debug=True)