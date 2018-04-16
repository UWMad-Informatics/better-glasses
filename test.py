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

# Get the tSNE plot
