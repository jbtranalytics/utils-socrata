from fastapi import FastAPI
from routers import socrata, pipelines, bigquery

# uvicorn --host=0.0.0.0 src.main:app

socrata_descr = (
"""
Defaults domain=data.lacity.org, dataset_id=dik5-hwp6 (LAX Parking).
"""
)



tags_metadata = [
    {
        "name": "Hello World!",
        "description": "Welcome!",
    },
    {
        "name": "Socrata",
        "description": socrata_descr

    },
    {
        "name": "BigQuery",
        "description": "Defaults domain=data.lacity.org, dataset_id=dik5-hwp6 (LAX Parking).",
    },
    {
        "name": "Pipelines",
        "description": "Defaults domain=data.lacity.org, dataset_id=dik5-hwp6 (LAX Parking).",
    },

]

app = FastAPI(
    openapi_tags=tags_metadata
)

app.include_router(socrata.router)
app.include_router(pipelines.router)
app.include_router(bigquery.router)

@app.get("/", tags=["Hello World!"])
def root():
    return {"message": "Hello World!"}




