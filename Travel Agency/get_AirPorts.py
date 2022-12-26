# import the requierd libraries
import json
import pandas as pd
import requests

# URL To get the airlines list
url = "https://flight-radar1.p.rapidapi.com/airports/list"

# Headers which contain the API Key
headers = {
        "X-RapidAPI-Key": "e8ceadd810msh0048b96168083d5p170c78jsnd21f2b796cf9",
        "X-RapidAPI-Host": "flight-radar1.p.rapidapi.com"
}

# request the url and get the response
response = requests.request("GET", url, headers=headers)

# format the response from text to json
json_response = json.loads(response.text)['rows']

# create a dataframe
df = pd.DataFrame.from_records(json_response)

# save the dataframe as a csv File
df.to_csv('AirPorts.csv')