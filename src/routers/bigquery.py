from fastapi import APIRouter, Depends
from schemas import FieldAgg


router = APIRouter(
    prefix="/bigquery",
    tags=['BigQuery']
    
)


@router.get("/dataset/exists")
def dataset_exists(dataset):
    pass


@router.get("/table/exists")
def table_exists(dataset, table):
    pass


@router.get("/table/field/agg")
def field_min(dataset, table, field, agg):
    pass


@router.get("/runsql")
def run_sql(sql):
    pass

