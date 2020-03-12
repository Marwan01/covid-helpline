from signalwire.relay.consumer import Consumer
from signalwire.rest import Client as signalwire_client
import pandas as pd 
from  datetime import  datetime,timedelta
import numpy as np
import pickle,json

global client, df,LOCATIONS,DEFAULT_RESPONSE,ADVICE, og_date,phone_data,phone_to
phone_to = '+16364749180'
og_date= "03-11-2020"
url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-11-2020.csv'
df = pd.read_csv(url)
df['Last Update']= df['Last Update'].apply(lambda x: x.split("T")[0])
df = df.replace(np.nan, '', regex=True)
LOCATIONS = list(df['Country/Region'].unique()) + list(df['Province/State'].unique())

client = signalwire_client("6c37ce1d-ee94-4b5b-961a-2fb9683933b2", "PT2cbd11afb7172b795e31508c411a20a7faef8c973e5ac2ac", signalwire_space_url = 'coronasmss.signalwire.com')

DEFAULT_RESPONSE ="""Welcome to the corona info line!
Text 'tips' to get information from the CDC about best practices
A location you want the most up to date report. EX: 'Missouri' or 'Italy'
If you want to sign up for daily updates in regards to corona updates text: 'Daily Italy' or 'Daily Washington'"""

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

def save_data_phone_numbers(data=None):
    if not data : 
        data = []
    pickle.dump( data, open( "phone_numbers.p", "wb" ) )
def load_data_phone_numbers():
    try:
        return pickle.load( open( "phone_numbers.p", "rb" ) )
    except:
        return {}

phone_data= load_data_phone_numbers()
def check_new_data(message_obj):
    now = datetime.now().strftime("%m-%d-%Y")
    if (now != "03-11-2020"):
        try:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{now}.csv'
            df = pd.read_csv(url)
            # TODO  send all sms when new data is ingested
            for phone, location, in phone_data.items():
                row_test = get_data_bas_location(location)
                msg_out = generate_message_from_row(row_test)
                send_text(msg_out,phone)
                og_date = datetime.now().strftime("%m-%d-%Y")
        except:
            print("NEW DAY NO NEW DATA")


def send_text(text,phone_to):
    message = client.messages.create(
                                from_='+13143470627',
                                body=text,
                                to=phone_to)
    print("sent")

def return_tips():
    return ADVICE

def eliminate_element_from_list(lis,element):
    return lis[:lis.index(element)]+ lis[lis.index(element)+1:]


def subscribe_daily(mess):
    location = mess.body.rstrip().split(" ")[1]    
    #TODO Store Object
    number_inbound = mess.from_number

    phone_data[number_inbound] = location

    save_data_phone_numbers(phone_data)
    return f"Thank you. You are now subsribed to daily messages for Corona Virus updates for {location}"

def get_data_bas_location(location):
    if (location == "US" or location == "China"):
        return ["",location,""]+ list(df[df['Country/Region'].str.contains(location)].groupby("Country/Region").sum().values[0])
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
    # print("---------MOCKSENT---------")

class CustomConsumer(Consumer):
    def setup(self):
        self.project = '6c IMMA TEXT YOU'
        self.token = 'PT IMMA TEXT YOU '
        self.contexts = ['corona-sms']
    async def on_incoming_message(self, message):
        print('Handle inbound task')
        print(message.body)
        handle_message(message)

# print(LOCATIONS)

consumer = CustomConsumer()
consumer.run()
