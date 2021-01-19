from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import pandas as pd
import geopandas as gpd

#Run docker inspect with the postgis container id to get the IP
ip = '0.0.0.0'
socket = '5432'
user = 'otuc'
password = 'otuc_test'

# Creating SQLAlchemy's engine to use
engine = create_engine(f'postgresql://{user}:{password}@{ip}:{socket}/otuc')

#Read hexagon and road test dataset
hexs = gpd.read_file('./data/hexs_speed.geojson')
# vias = gpd.read_file('./data/vias_speed.geojson')

hexs['geom'] = hexs['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
# vias['geom'] = vias['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))

#drop the geometry column as it is now duplicative
hexs.drop('geometry', 1, inplace=True)
# vias.drop('geometry', 1, inplace=True)

hexs = hexs[(~pd.isnull(hexs['LOCATION_CREATED'])) | (~pd.isnull(hexs['LOCATION_SPEED']))]

hexs.loc[:,'year'] = hexs.loc[:,'LOCATION_CREATED'].apply(lambda x: int(x[:4]))
hexs.loc[:,'month'] = hexs.loc[:,'LOCATION_CREATED'].apply(lambda x: int(x[5:7]))
hexs.loc[:,'day'] = hexs.loc[:,'LOCATION_CREATED'].apply(lambda x: int(x[8:10]))
hexs.loc[:,'hour'] = hexs.loc[:, 'LOCATION_CREATED'].apply(lambda x: int(x[11:13]))
hexs.loc[:,'minute'] = hexs.loc[:,'LOCATION_CREATED'].apply(lambda x: int(x[14:16]))

del hexs['LOCATION_CREATED']

# Use 'dtype' to specify column's type
# For the geom column, we will use GeoAlchemy's type 'Geometry'
hexs.to_sql('hexagons', engine, if_exists='append', index=False,
                         dtype={'geom': Geometry('POLYGON', srid=4326)})

# vias.to_sql('vias', engine, if_exists='append', index=False,
#                          dtype={'geom': Geometry('LINESTRING', srid=4326)})
