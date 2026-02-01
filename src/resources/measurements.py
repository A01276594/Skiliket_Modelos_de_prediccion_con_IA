import requests
import csv
import json
BASE_URL = "https://app.skiliket.net/server/api/v1"
url = f"{BASE_URL}/devices/1/devicemeasurements/types"
response = requests.get(url)
print(response.json())
