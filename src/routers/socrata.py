from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from classes import MySocrata
from schemas import StreamType, SocrataBaseParams, SocrataDataParams


router = APIRouter(
    prefix="/socrata",
    tags=['Socrata']
    
)


@router.get("/metadata")
def get_metadata(params: SocrataBaseParams = Depends()):
    mysocrata = MySocrata()
    response = mysocrata.get_meta(domain=params.domain, dataset_id=params.dataset_id)
    return response


@router.get("/schema")
def get_schema(params: SocrataBaseParams = Depends()):
    mysocrata = MySocrata()
    response = mysocrata.get_schema(domain=params.domain, dataset_id=params.dataset_id)
    return response


@router.get("/datapage")
def get_datapage(params: SocrataDataParams = Depends()):
    mysocrata = MySocrata()
    response = mysocrata.get_data(domain=params.domain, dataset_id=params.dataset_id, pagesize=params.pagesize, where=params.where)
    return response


@router.get("/datastream")
def get_datastream(params: SocrataDataParams = Depends(), streamtype: StreamType=StreamType.JSONRECORDS):
    mysocrata = MySocrata()
    response = mysocrata.get_datastream(domain=params.domain, dataset_id=params.dataset_id, pagesize=params.pagesize, where=params.where, streamtype=streamtype)
    return StreamingResponse(response)


