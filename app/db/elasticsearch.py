from tempfile import tempdir
from textwrap import indent
from typing import List
from xmlrpc.client import Boolean
from assets.document import Document, DocumentFields
from core.config import settings
import httpx

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
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/users/_doc/{username}'
        response = await client.get(URI, headers=self.headers)
        print('password: ' + password)
        if response.json()['found']:
          return response.json()['_source']['password'] == password
        else:
          return False
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

  async def add_user_search_tag(self, username, tag_label, result_ids, search):
    tag_doc = {
      "label": tag_label,
      "owner": username,
      "result_ids": result_ids,
      "search": search
    }
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/user_tags/_doc'
        response = await client.post(URI, headers=self.headers, json=tag_doc)
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)


  async def suggest_user_search_tags(self, substr: str):
    query = {
      "suggest": {
        "tag_suggestion" : {
          "text" : substr,
          "term" : {
            "field" : "label"
          }
        }
      }
    }
    
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/user_tags/_search'
        response = await client.post(URI, headers=self.headers, json=query)
        response_json = response.json()
        print("baana1")
        print(response_json)
        suggestion_objects = response_json["suggest"]["tag_suggestion"][0]["options"]
        suggestion_labels = [obj["text"] for obj in suggestion_objects]
        print("suggestion_labels:")
        print(suggestion_labels)
        tags = list()
        for label in suggestion_labels:
          query = {
            "query": {
              "term" : {
                "label": label
              }
            }
          }
          URI = f'{settings.ES_API}/user_tags/_search'
          response = await client.post(URI, headers=self.headers, json=query)
          result_obj = response.json()["hits"]["hits"][0]
          tags.append({
            "id": result_obj["_id"],
            "name": result_obj["_source"]["label"],
            "owner": result_obj["_source"]["owner"],
            "result_ids": result_obj["_source"]["result_ids"]
          })
        return tags
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