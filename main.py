import geopandas as gpd
from sqlalchemy import create_engine
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class HexOTUC(BaseModel):
    year: str
    month: str
    day: str
    hour: str
    minute: str

class NetworkOTUC(BaseModel):
    start_date: str
    end_date: str

origins = [
    "*",
    "http://localhost",
    "http://localhost:8000",
]

ip = 'localhost'#'0.0.0.0'
socket = '5432'
user = 'otuc'
password = 'otuc_test'

# Creating SQLAlchemy's engine to use
engine = create_engine(f'postgresql://{user}:{password}@{ip}:{socket}/otuc')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/hexagons/')
async def get_hex_data(model: NetworkOTUC):
    sql = '''
    SELECT hex, avg("LOCATION_SPEED") as mean_speed, geom FROM hexagons WHERE date BETWEEN DATE '{}' and DATE '{}'
    GROUP BY hex, geom
    '''.format(model.start_date, model.end_date)

    with engine.connect() as connection:
        gdf = gpd.read_postgis(sql, connection)

    return gdf.__geo_interface__

@app.post('/network/')
async def get_arc_data(model: NetworkOTUC):
    sql = '''
    SELECT index, avg("LOCATION_SPEED") as mean_speed, geom FROM network WHERE date BETWEEN DATE '{}' and DATE '{}'
    GROUP BY index, geom
    '''.format(model.start_date, model.end_date)

    with engine.connect() as connection:
        gdf = gpd.read_postgis(sql, connection)

    return gdf.__geo_interface__
