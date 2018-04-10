import os
import sys
import json
import requests
import datetime
from citrination_client.client import CitrinationClient
from citrination_client.util.quote_finder import quote

# Set up client
api_key = os.environ['CITRINATION_API_KEY']
client = CitrinationClient(api_key)
api_url = 'https://citrination.com/api'
headers = {'X-API-Key': quote(api_key), 'Content-Type': 'application/json'}

# Go to Data View URL and save results from predictions to json
#plot = client.estimators(str(1356))
url = api_url + '/data_views/' + str(4291) + '/estimators'
result = requests.get(url, headers=headers)
if result.status_code == 200:
    plot = json.loads(result.content.decode('utf-8'))
else:
    print('An error ocurred during this action: ' + str(result.status_code) + ' - ' + str(result.reason) )
    print(result.content)
    sys.exit()

# Write predicted values in json to a file.
# Add date and time to file name
date_and_time = datetime.datetime.now()
with open('plot_data_' + str(date_and_time) + ".txt", 'w') as outfile:
    json.dump(plot, outfile)