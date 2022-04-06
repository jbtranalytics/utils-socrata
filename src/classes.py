import json
from tkinter import PROJECTING
import pandas as pd
from sodapy import Socrata
from schemas import MetaDataSchema, StreamType
from google.cloud import bigquery


class MySocrata():
    def __init__(self) -> None:
        pass


    def set_client(self, domain):
        self.client = Socrata(
            domain,
            app_token=None
        )


    def get_meta(self, domain=str, dataset_id=str) -> dict:
        self.set_client(domain)
        return self.client.get_metadata(dataset_id)


    def get_schema(self, domain: str, dataset_id: str):
        response = self.get_meta(domain, dataset_id)
        return MetaDataSchema(**response)


   # returns a list of dictionaries
    def get_data(self, domain: str, dataset_id: str, pagesize: int, where: str=None):
        if not where:
            where = ""

        limit = pagesize

        self.set_client(domain)
        response = self.client.get(
            dataset_id,
            limit=limit,
            where=where
        )
        # print(type(response)) #list
        # for item in response:
        #     print(type(item)) #dict
        return response
    
    # returns a generator.
    def get_datastream(self, domain: str, dataset_id: str, pagesize: int, where: str=None, streamtype: StreamType=StreamType.JSONRECORDS, streamlistdict: bool=False):
        if not where:
            where = ""
        page = 1
        limit = pagesize
        offset = 0
        first = True
        self.set_client(domain)
        
        if streamlistdict:
            pass
        else:
            zipper1 = [StreamType.JSONRECORDS, StreamType.JSONPAGES]
            zipper2 = ['[\n','{\n']
            zipper3 = ['\n]','\n}']
            
            for x, y in zip(zipper1, zipper2):
                if streamtype == x:
                    yield y

        while True:
            response = self.client.get(
                dataset_id,
                limit=limit,
                where=where,
                offset=offset
            )

            if streamlistdict:
                if len(response) != 0:
                    yield response
                else:
                    return
            else:
                if streamtype == StreamType.JSONRECORDS:
                    for item in response:
                        if first:
                            prefix = ""
                            first = False
                        else:
                            prefix = ",\n"
                        yield prefix + json.dumps(item, indent=4)
                elif streamtype == StreamType.JSONPAGES:
                    if len(response) != 0:
                        if first:
                            prefix = f'"page_{page}": '
                            first = False
                        else:
                            prefix = f',\n"page_{page}": '
                        yield prefix + json.dumps(response, indent=4)                    
                else:
                    return

            if len(response) < limit:
                if streamlistdict:
                    pass
                else:
                    for x, y in zip(zipper1, zipper3):
                        if streamtype == x:
                            yield y
                return

            offset += limit

            # safety condition to prevent infinite loops while debuging
            # if page > 100:
            #     yield '{"ERROR":"Max pages of 100 Reached. Try increasing page size. Or in infinite loop."}]'
            #     return
            page += 1
    

    def datastream_to_dataframe(self, domain: str, dataset_id: str, pagesize: int, where: str=None):
        datastream = self.get_datastream(domain=domain, dataset_id=dataset_id, pagesize=pagesize, where=where, streamlistdict=True)
        for listdict in datastream:
            df = pd.DataFrame.from_records(listdict)
            # do something with dataframe
            x = df.info()
            print(type(x))


            
class MyBigQuery():
    def __init__(self, project, dataset) -> None:
        self.project = project
        pass
            
    
    def set_client(self):
        self.client = bigquery.Client()


    def run_sql(self, sql: str):
        job = self.client(sql)
        return job.results()


    def get_field_agg(self, project: str, dataset: str, table: str, field: str, agg: str):
        sql = f" SELECT {agg}({field}) AS agg FROM `{project}.{dataset}.{table}` LIMIT 1"
        results = self.run_sql(sql)
        for row in results:
            return row[0]
    