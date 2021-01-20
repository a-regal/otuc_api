import requests
import json
import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

#Setup url to request
endpoint = 'http://127.0.0.1:8000/hexagons/'

#Filter params for hex data
payload = {'year':'2018', 'month':'9', 'day':'7', 'hour':'23', 'minute':'48'}

#Profit
response = requests.post(endpoint, json=payload)

print(response.json())

# with open('./hexs_speed.geojson', 'w')  as f:
#     f.write(json.dumps(response.json()))

ip = '0.0.0.0'
socket = '5432'
user = 'otuc'
password = 'otuc_test'

# Creating SQLAlchemy's engine to use
engine = create_engine(f'postgresql://{user}:{password}@{ip}:{socket}/otuc')

#hex, avg('LOCATION_SPEED'), geom
#GROUP BY hex, geom
sql = f'''
SELECT hex, avg("LOCATION_SPEED") as mean_speed, geom FROM hexagons WHERE year = {int(payload['year'])} AND month = {int(payload['month'])}
AND day = {int(payload['day'])} AND hour = {int(payload['hour'])} AND minute = {int(payload['minute'])}
GROUP BY hex, geom
'''

gdf = gpd.read_postgis(sql, engine)

print(gdf.head())
print(gdf.dtypes)
gdf.plot(column='mean_speed')
plt.show()
