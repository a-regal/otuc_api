import geopandas as gpd
from sqlalchemy import create_engine
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class OtucData(BaseModel):
    year: str
    month: str
    day: str
    hour: str
    minute: str

origins = [
    "*",
    "http://localhost",
    "http://localhost:8000",
]

ip = '0.0.0.0'
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
async def get_hex_data(model: OtucData):
    sql = f'''
    SELECT hex, avg("LOCATION_SPEED") as mean_speed, geom FROM hexagons WHERE year = {int(model.year)} AND month = {int(model.month)}
    AND day = {int(model.day)} AND hour = {int(model.hour)} AND minute = {int(model.minute)}
    GROUP BY hex, geom
    '''

    with engine.connect() as connection:
        gdf = gpd.read_postgis(sql, connection)

    return gdf.__geo_interface__
