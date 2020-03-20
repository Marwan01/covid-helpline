## US DOCUMENTATION: https://pypi.org/project/us/
import us
## USZIPCODE DOCUMENTATION: https://pypi.org/project/uszipcode/
from uszipcode import SearchEngine

import pandas as pd 

def get_state_stats(zip_code):
    
    try:
        data = pd.read_csv("confirmed_cases.csv")

        search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
        zip_code_data = search.by_zipcode(zip_code).to_dict()

        if(zip_code_data['state'] is not None):
            # JHU IS NOT REPORTING UPDATED COUNTY LEVEL DATA
            # if(zip_code_data['county'] is not None):
            #     county_name = zip_code_data['county'] 
            #     county_data = data[data['Province/State'].str.contains(county_name, na=False)]
            #     county_number_cases_today = county_data.iloc[:,-1].iloc[0]
            #     county_number_cases_yesterday = county_data.iloc[:,-2].iloc[0]
            #     print(county_data)
            #     county_growth_rate = ((county_number_cases_today-county_number_cases_yesterday)/county_number_cases_yesterday)*100
            #     county_growth_rate_str = '%.3f'%(county_growth_rate)
            #     county_response = f"Today, {county_name} has {county_number_cases_today} confirmed cases of Covid-19.  There were {county_number_cases_yesterday} cases reported yesterday, a growth rate of +{county_growth_rate_str}%."
            #     print(county_response)

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
            response = f"Today, {state_name} has {state_number_cases_today} confirmed cases of Covid-19.  There were {state_number_cases_yesterday} cases reported yesterday, a growth rate of {change_sign}{growth_rate_str}%."
        else:
            response = "We do not have data on this zip code.  Are you sure you entered it properly?  It should be 5 digits long, and must be in the United States."
        return response
    except:
        return "We do not have data on this zip code.  Are you sure you entered it properly?  It should be 5 digits long, and must be in the United States."

