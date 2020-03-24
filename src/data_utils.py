from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from responses import *

def load_csv():
    date = datetime.now().strftime("%m-%d-%Y")
    counter = 1
    while True:
        try:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'
            df = pd.read_csv(url)

            return df
        except:
            print("Report wasn't found moving one day back...")
            date = (datetime.now() - timedelta(counter)).strftime("%m-%d-%Y")
            counter += 1

def load_data():
    df = load_csv()
    df['Last Update'] = df['Last Update'].apply(lambda x: x.split("T")[0])
    df = df.replace(np.nan, '', regex=True)
    locations = list(df['Combined_Key'].unique())
    return df, locations

def get_data_bas_location(location, df):
    if location.lower() == "US".lower() or  location.lower() == "USA".lower():
        return ["", location, ""] + list(
             df[df['Country/Region'].str.contains("US")].groupby("Country/Region").sum().values[0])
    try:
        dd = df[df['Province/State'].str.contains(location)].values[0]
    except:
        dd = df[df['Country/Region'].str.contains(location)].values[0]
    return list(dd)


def generate_message_from_row(row):
    message = f'Today\'s Covid-19 Report in {row[0].upper()} {row[1].upper()}:\n' \
              f'Confirmed: {row[3]} \n' \
              f'Recovered: {row[5]} \n' \
              f'Deaths: {row[4]}\n' \
              f'as of {datetime.now().strftime("%B %d, %Y")} '
    message = message.replace("  ", " ")
    return message


def handle_message_location(location,df):
    row = get_data_bas_location(location, df)
    msg_out = generate_message_from_row(row)
    return msg_out


def load_data_sms(bucket):
    data = {}
    for b in bucket.list_blobs(prefix='sub/'):
        blob_path = b.name
        b1 = blob_path[blob_path.find("+1")+2:blob_path.rfind("/")]
        data[b1] = b.download_as_string().decode('utf-8')
    return data
