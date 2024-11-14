# import necessary packages
import pandas as pd
import requests

# read in API Key
with open('api.txt', 'r') as file:
    fred_key = file.read()

#create list of variable IDs for my dataset
ids = ['FEDFUNDS', 'CPIAUCSL', 'PAYEMS', 'UNRATE', 'LNS11300002', 'GDP', 
       'CIVPART', 'A939RX0Q048SBEA', 'CES0500000003']

i = 0
while i < (len(ids)): #initialize while loop to API request for each ID
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={ids[i]}&api_key={api_key}&file_type=json"
    response = requests.get(url)

    data = response.json() 
    variable = pd.DataFrame(data['observations']) # turn requested data into a dataframe
    variable.drop(['realtime_start', 'realtime_end'],axis = 1, inplace = True) 
    variable.columns = ['Date', ids[i]] #drop and rename columns

    if i == 5: # The first 4 values of the GDP ID are just '.' so they need to be removed
        variable = variable.iloc[4:]

    if i == 0: # create dataframe of all variables
        df = pd.DataFrame(variable)
    else:
        df = df.merge(variable, on = 'Date', how = 'outer')
    i += 1

# rename columns to proper names
df.columns = ['Date','Fin_Market_Interest_Rates', 'CPI', 'Num_of_Workers(thousands)','Unemployment_Rate',
'Work_Partic_Rate_Women', 'GDP(billions)', 'Work_Partic_Rate_All', 'Real_GDP_per_Capita', 'Hourly_Wages_Private($)']

# set each variable to the correct data type
df = df.astype({'Fin_Market_Interest_Rates': float, 'CPI': float, 'Num_of_Workers(thousands)': int, 
                'Unemployment_Rate' : float,'Work_Partic_Rate_Women' : float, 'GDP(billions)': float, 
                 'Work_Partic_Rate_All' : float, 'Real_GDP_per_Capita' : float, 'Hourly_Wages_Private($)' : float})
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Note: not every variable in my dataframe has a value for every row, because each variable has been tracked for a different amount of time

