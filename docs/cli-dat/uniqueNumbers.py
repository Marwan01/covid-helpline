#Importing libraries
import numpy as np
import datetime
from twilio.rest import Client
import numpy as np
from datetime import datetime
from pytz import timezone
from io import StringIO

#Cli secrets (need to add to .gitignore)
client = Client("", "")

#Fetching messages from cli
def get_total_exchanged():
    messages = client.messages.list(to="+19142684399")

#Creating new array to store vaules
z=[]

#Creating a defintion for the amount of unique phone numbers
for sms in client.messages.list():
    z = (sms.to.split() + z)

#The list is converted into a set so that duplicated numbers are removed
myset = set(z)

#Creating new variable to store all exchanged phone numbers
uniqueNumbers = len(myset)

#Feedback message
print("There are " + str(uniqueNumbers) + " unique callers.")

#Resetting the set into a list to do further calculations
mynewlist = list(myset)
