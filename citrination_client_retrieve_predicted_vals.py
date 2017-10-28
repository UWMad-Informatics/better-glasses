import os
import sys
import json
import requests
from citrination_client.client import CitrinationClient
from citrination_client.util.quote_finder import quote

api_key = os.environ['CITRINATION_API_KEY']
client = CitrinationClient(api_key)
api_url = 'https://citrination.com/api'
headers = {'X-API-Key': quote(api_key), 'Content-Type': 'application/json'}

#plot = client.estimators(str(1356))
url = api_url + '/data_views/' + str(1739) + '/estimators'
result = requests.get(url, headers=headers)
if result.status_code == 200:
    plot = json.loads(result.content.decode('utf-8'))
else:
    print('An error ocurred during this action: ' + str(result.status_code) + ' - ' + str(result.reason) )
    print(result.content)
    sys.exit()

with open('plot_data.txt', 'w') as outfile:
    json.dump(plot, outfile)
