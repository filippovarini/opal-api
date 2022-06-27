from tempfile import tempdir
from textwrap import indent
from typing import List
from xmlrpc.client import Boolean
from assets.document import Document, DocumentFields
from core.config import settings
import httpx
import random
import json

class ElasticSearchQuery:
  def __init__(self):
    self.must_fields = []
    self.should_fields = []
    self.must_not_fields = []
    self.top_level_fields = ["format", "tags"]

  def add_date_range(self, lower_limit: str, upper_limit: str):
    self.must_fields.append({"range" : {
      "fields.date" : { "gte" : lower_limit, "lte" : upper_limit }
    }})

  def add_term_search(self, field: str, term: str):
    field_prefix = ""
    if field not in self.top_level_fields:
      field_prefix = "fields."
    self.should_fields.append({
      "match": {(field_prefix + field): term}
    })

  def add_negative_term_search(self, field: str, term: str):
    field_prefix = ""
    if field not in self.top_level_fields:
      field_prefix = "fields."
    self.must_not_fields.append({
      "match": {field_prefix + field: term}
    })

  def build_query(self):
    query = {"query": {
      "bool": {}
    }}
    if self.must_fields:
      query["query"]["bool"]["must"] = self.must_fields
    if self.should_fields:
      query["query"]["bool"]["should"] = self.should_fields
    if self.must_not_fields:
      query["query"]["bool"]["must_not"] = self.must_not_fields
    return query
  

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

  # creates a new user in elasticsearch
  async def create_user(self, username: str, password: str) -> Boolean:
    query = {
      "username": username,
      "password": password
    }
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/users/_doc/{username}'
        response = await client.post(self.URI, headers=self.headers, json=query)
        return True
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

  # checks that the correct password has been supplied for a particular user
  async def auth_user(self, username: str, password: str) -> Boolean:
    try:
      URI = f'{settings.ES_API}/users/_doc/{username}'
      response = await client.get(URI, headers=self.headers)
      if response.json()['found']:
        return response.json()['_source']['password'] == password
      else:
        return False
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
    if len(tags) > 0:
      filters.append(tagQuery)

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

  async def get_from_search_query(self, query: ElasticSearchQuery):
    async with httpx.AsyncClient() as client:
      try:
        print(query.build_query())
        response = await client.post(self.URI, headers=self.headers, json=query.build_query())
        docs = response.json()['hits']['hits']
        return [Document(**{'id': doc['_id'], **doc['_source']}) for doc in docs]

      # TODO: handle errors
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

elasticSearch = ElasticSearch()