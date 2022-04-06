from fastapi import APIRouter, Depends
from classes import MySocrata
from schemas import SocrataDataParams


router = APIRouter(
    prefix="/pipelines",
    tags=['Pipelines']
    
)


@router.get("/socratatobigquery")
def run_socratatobigquery(params: SocrataDataParams = Depends() ):
    mysocrata = MySocrata()
    mysocrata.datastream_to_dataframe(domain=params.domain, dataset_id=params.dataset_id, pagesize=params.pagesize, where=params.where)
    return {"message": "do something success"}