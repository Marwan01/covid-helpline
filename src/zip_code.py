## US DOCUMENTATION: https://pypi.org/project/us/
import us
## USZIPCODE DOCUMENTATION: https://pypi.org/project/uszipcode/
from uszipcode import SearchEngine

import pandas as pd 

def get_state_stats(zip_code):
    

    data = pd.read_csv("confirmed_cases.csv")

    search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
    zip_code_data = search.by_zipcode(zip_code).to_dict()
    county_response=""
    state_response=""
    if(zip_code_data['state'] is not None):

        if(zip_code_data['county'] is not None):
            county_data = pd.read_csv("county_cases.csv")

            county_name = zip_code_data['county'] 

            county_data = county_data[ (county_data['county'] == county_name) & (county_data['state'] == zip_code_data['state']) ]
            if(county_data.shape[0]>0):
                county_number_cases_today = int(county_data.iloc[:,-1].iloc[0])
                county_number_cases_yesterday = int(county_data.iloc[:,-2].iloc[0])
                if(county_number_cases_yesterday > 0 ):
                    county_growth_rate = ((county_number_cases_today-county_number_cases_yesterday)/county_number_cases_yesterday)*100
                    county_growth_rate_str = '%.3f'%(county_growth_rate)
                    county_response = f"{county_name.upper()}\nToday: {county_number_cases_today} confirmed cases of Covid-19 \nYesterday: {county_number_cases_yesterday} confirmed cases \nGrowth Rate: +{county_growth_rate_str}%\n"
                else:
                    county_response = f"{county_name.upper()}\nToday: {county_number_cases_today} confirmed cases of Covid-19\n"
                city_url = zip_code_data['major_city'].replace(" ", "%20")
                county_response+=f"Latest updates from your mayor: https://twitter.com/search?q={city_url}%20mayor&f=user\n\n"

        state_abbreviation = zip_code_data['state']
        state_name = us.states.lookup(state_abbreviation).name
        state_data = data[ data['Province/State'] == state_name ]
        state_number_cases_today = state_data.iloc[:,-1].iloc[0]
        state_number_cases_yesterday = state_data.iloc[:,-2].iloc[0]
        growth_rate = ((state_number_cases_today-state_number_cases_yesterday)/state_number_cases_yesterday)*100
        growth_rate_str = '%.3f'%(growth_rate)
        change_sign = ""
        if(growth_rate>0):
            change_sign="+"
        else:
            change_sign = "-"
        state_response = f"{state_name.upper()}\nToday: {state_number_cases_today} confirmed cases of Covid-19  \nYesterday: {state_number_cases_yesterday} confirmed cases \nGrowth Rate: {change_sign}{growth_rate_str}%\n"
        state_url = state_name.replace(" ", "%20")
        state_response+=f"Latest updates from your governor: https://twitter.com/search?q={state_url}%20governor&f=user"

    else:
        state_response = "We do not have data on this zip code.  Are you sure you entered it properly?  It should be 5 digits long, and must be in the United States."
    return county_response+state_response
   

print(get_state_stats("94710"))