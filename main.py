import geopandas as gpd
from sqlalchemy import create_engine
from fastapi import FastAPI
from pydantic import BaseModel

class OtucData(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int


ip = '0.0.0.0'
socket = '5432'
user = 'otuc'
password = 'otuc_test'

# Creating SQLAlchemy's engine to use
engine = create_engine(f'postgresql://{user}:{password}@{ip}:{socket}/otuc')

app = FastAPI()

@app.post('/hexagons/')
async def get_hex_data(model: OtucData):
    sql = f'''
    SELECT * FROM hexagons WHERE year = {model.year} AND month = {model.month} AND day = {model.day} AND hour = {model.hour} AND minute = {model.minute}
    '''

    with engine.connect() as connection:
        gdf = gpd.read_postgis(sql, connection)

    return gdf.__geo_interface__
