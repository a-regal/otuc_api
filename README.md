# otuc_api
A simple FastAPI implementation for the OTUC PostGIS database.

To run the API, first create a toy dataset using the ``` create_postgis.sh ``` script.
After that, make sure the container is running and upload some toy data using upload_geojson.
With the database complete, run ```bash uvicorn main:app``` and enjoy making requests!
