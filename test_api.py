import requests

#Setup url to request
endpoint = 'http://127.0.0.1:8000/hexagons'

#Filter params for hex data
payload = {'year':2018, 'month':9, 'day':7, 'hour':23, 'minute':48}

#Profit
response = requests.post(endpoint, json=payload)

print(response.json())
