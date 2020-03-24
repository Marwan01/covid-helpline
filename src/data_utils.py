from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from responses import *
import r
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
    df['Last Update']=df['Last_Update'].apply( lambda text : re.search(r'\d{4}-\d{2}-\d{2}', text).group())
    df = df.replace(np.nan, '', regex=True)
    locations = list(df['Combined_Key'].unique())
    return df, locations

def get_data_bas_location(location, df):
    try:
        dd = df[df['Combined_Key'].str.contains(location)].values[0]
    except:
        dd = df[df['Country_Region'].str.contains(location)].values[0]
    return list(dd)


def generate_message_from_row(row):
    message = f'In {row[11]}:\n' \
              f'{int(row[7])} confirmed, \n' \
              f'{int(row[9])} recovered, \n' \
              f'and {int(row[8])} deaths\n' \
              f'as of {datetime.now().strftime("%B %d, %Y")}. '
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
