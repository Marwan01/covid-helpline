## US DOCUMENTATION: https://pypi.org/project/us/
import us
## USZIPCODE DOCUMENTATION: https://pypi.org/project/uszipcode/
from uszipcode import SearchEngine
from datetime import datetime, timedelta

import pandas as pd 

today_date = datetime.now().strftime("%m-%d-%Y")

# fix
def load_df(url):
    return pd.read_csv(url)


def load_state_daily_report():
    date = datetime.now().strftime("%m-%d-%Y")
    counter = 1
    while True:
        try:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'
            df = pd.read_csv(url)
            df = df.rename(columns={'Province_State':'Province/State','Country_Region':'Country/Region'})
            ## HOT FIX FOR JHU DATA SCHEMA ISSUE: https://github.com/CSSEGISandData/COVID-19/issues/1326
            # print(df.head())

            return df
        except:
            print("Report wasn't found moving one day back...")
            date = (datetime.now() - timedelta(counter)).strftime("%m-%d-%Y")
            counter += 1

def get_zip_code_stats(zip_code):
    
    state_data_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    data = load_df(state_data_url)

    search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
    zip_code_data = search.by_zipcode(zip_code).to_dict()
    county_response=""

   
    if(zip_code_data['state'] is not None):
        
        if(zip_code_data['county'] is not None):
            county_data_url = 'https://coronadatascraper.com/timeseries-jhu.csv'
            county_data = load_df(county_data_url)

            county_name = zip_code_data['county'] 

            county_data = county_data[ (county_data['county'] == county_name) & (county_data['state'] == zip_code_data['state']) ].fillna(0)
            if(county_data.shape[0]>0):
                # print(county_data.head())
                county_number_cases_today = int(county_data.iloc[:,-1].iloc[0])
                county_number_cases_yesterday = int(county_data.iloc[:,-2].iloc[0])
                # unused variable
                county_url = county_data.iloc[:,7].iloc[0]
                if(county_number_cases_yesterday > 0 and county_number_cases_today > 0 and (county_number_cases_today-county_number_cases_yesterday>0) ):
                    county_growth_rate = ((county_number_cases_today-county_number_cases_yesterday)/county_number_cases_yesterday)*100
                    county_growth_rate_str = '%.3f'%(county_growth_rate)
                    county_response = f"Today\'s Covid-19 Report in:\n {county_name.upper()}:\n Confirmed: {county_number_cases_today}\n as of {today_date}\nYesterday: {state_number_cases_yesterday} confirmed cases \nDaily Growth Rate: {change_sign}{growth_rate_str}%"
                elif(county_number_cases_today > 0 ):
                    county_response = f"Today\'s Covid-19 Report in:\n {county_name.upper()}:\n Confirmed: {county_number_cases_today}\n as of {today_date}\nYesterday: {state_number_cases_yesterday} confirmed cases \nDaily Growth Rate: {change_sign}{growth_rate_str}%"
                # unused variable
                city_url = zip_code_data['major_city'].replace(" ", "%20")
                # county_response+=f"Latest updates from your mayor: https://twitter.com/search?q={city_url}%20mayor&f=user\n\n"
                # county_response+=f"Source: {county_url}\n\n"

                county_response+=f"\n"


        state_abbreviation = zip_code_data['state']
        state_name = us.states.lookup(state_abbreviation).name
        state_data = data[ data['Province/State'] == state_name ]
        state_number_cases_today = state_data.iloc[:,-1].iloc[0]
        state_number_cases_yesterday = state_data.iloc[:,-2].iloc[0]
        growth_rate = ((state_number_cases_today-state_number_cases_yesterday)/state_number_cases_yesterday)*100
        growth_rate_str = '%.3f'%(growth_rate)

        if(growth_rate>0):
            change_sign="+"
        else:
            change_sign = "-"
        
        daily_stats_df = load_state_daily_report()
        state_stats = daily_stats_df[ daily_stats_df['Province/State'] == state_name]
        state_deaths = state_stats.iloc[:,-4].iloc[0]
        state_recovered = state_stats.iloc[:,-3].iloc[0]
      
        # state_response = f"{state_name.upper()}\nToday: {state_number_cases_today} confirmed cases of Covid-19  \nYesterday: {state_number_cases_yesterday} confirmed cases \nGrowth Rate: {change_sign}{growth_rate_str}%\nDeaths: {state_deaths}\nRecovered: {state_recovered}"
        state_response = f"{state_name.upper()}\nToday: {state_number_cases_today} confirmed cases of Covid-19."


        # unused variable
        state_url = state_name.replace(" ", "%20")
        # state_response+=f"Latest updates from your governor: https://twitter.com/search?q={state_url}%20governor&f=user"

    else:
        state_response = "We do not have data on this zip code.  Are you sure you entered it properly?  It should be 5 digits long, and must be in the United States."
    return county_response+state_response
   
