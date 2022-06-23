from textwrap import indent
from typing import List
from assets.document import Document, DocumentFields
from core.config import settings
import httpx
import random
import json

class ElasticSearch():
  URI = f'{settings.ES_API}/{settings.DOC_INDEX}/_search'
  POST_URI = f'{settings.ES_API}/{settings.DOC_INDEX}/_doc'
  RESULT_SIZE = 100

  def __init__(self) -> None:
    self.headers = {
      "Content-Type": "application/json",
      "Authorization": f'Basic {settings.encode_credentials()}'
    }
  # Gets list of al documents and returns them in the Document class type
  async def get_all_documents(self) -> Document:
    async with httpx.AsyncClient() as client:
      try:
        response = await client.get(self.URI, headers=self.headers)
        docs = response.json()['hits']['hits']
        return [Document(**{'id': doc['_id'], **doc['_source']}) for doc in docs]

      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

  # Searches the document from metadata stored in our DB (tags, fiels)
  async def get_from_meta(self, tags: List[str], fieldsModel: DocumentFields) -> Document:
    tagQuery = {
      "terms_set": {
        "tags": {
        "terms": tags,
        "minimum_should_match_script": {
            "source": "params.num_terms"
          }
        }
      }
    }
    
    filters = []
    # if len(tags) > 0:
    #   filters.append(tagQuery)

    if fieldsModel: 
      fields = fieldsModel.dict()
      fieldQuery = [{"match": {f'fields.{key}': fields[key]}} for key in fields if fields[key]]
      filters += fieldQuery
    
    query = {
      "query": {
        "bool": {
          "filter": filters
        }
      },
      "size": self.RESULT_SIZE
    }

    async with httpx.AsyncClient() as client:
      try:
        response = await client.post(self.URI, headers=self.headers, json=query)
        docs = response.json()['hits']['hits']
        return [Document(**{'id': doc['_id'], **doc['_source']}) for doc in docs]

      # TODO: handle errors
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

elasticSearch = ElasticSearch()