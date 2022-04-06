from pydantic import BaseModel, root_validator
from enum import Enum


# Socrata

default_domain = "data.lacity.org"
default_dataset_id = "dik5-hwp6" #LAX Parking
default_pagesize = 1000
default_where = None

# BigQuery

default_project = ""
default_dataset = ""


class FieldAgg(str, Enum):
    MAX="MAX"
    MIN="MIN"
    COUNT="COUNT"


class BigQueryBaseParams():
    def __init__(self, project: str=default_project, dataset: str=default_dataset):
        self.project = project
        self.dataset = dataset


class BigQueryBaseParams():
    def __init__(self, project: str=default_project, dataset: str=default_dataset, table: str=None):
        self.project = project
        self.dataset = dataset
        self.table = table


class SocrataBaseParams():
    def __init__(self, domain: str=default_domain, dataset_id: str=default_dataset_id):
        self.domain = domain
        self.dataset_id = dataset_id


class SocrataDataParams():
    def __init__(self, domain: str=default_domain, dataset_id: str=default_dataset_id, pagesize: int=default_pagesize, where: str=default_where):
        self.domain = domain
        self.dataset_id = dataset_id
        self.pagesize = pagesize
        self.where = where


class StreamType(str, Enum):
    JSONRECORDS="JSONRECORDS"
    JSONPAGES="JSONPAGES"


class MetaDataSchema(BaseModel):
    id: str
    name: str
    displayType: str
    columns: list

    @root_validator
    def set_values(cls, values):
        raw = [x for x in values['columns'] if x['fieldName'].startswith(':')==False]
        values['columns'] = [x['fieldName'] for x in raw]
        values['columntypes'] = {x['fieldName']:x['dataTypeName'] for x in raw}
        values['columndates'] = [k for (k,v) in values['columntypes'].items() if v == "calendar_date"]
        values['columnnumbers'] = [k for (k,v) in values['columntypes'].items() if v == "number"]
        return values