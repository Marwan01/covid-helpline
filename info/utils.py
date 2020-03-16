import pandas as pd
from datetime import datetime, timedelta
from urllib.error import HTTPError
import numpy as np


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
    if location == "US" or location == "China":
        return ["", location, ""] + list(
             df[df['Country/Region'].str.contains(location)].groupby("Country/Region").sum().values[0])
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


def handle_message(location):

    df, locations = load_data()

    if location in locations:
        #rows = get_data_bas_location(location, df)
        row = get_data_bas_location(location, df)
        #msg_out = "\n\n".join(generate_message_from_row(row) for row in rows)
        msg_out = generate_message_from_row(row)
    else:
        msg_out = "There is no data for this location or check you spelling"

    return msg_out
