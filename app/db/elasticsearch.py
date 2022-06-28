from tempfile import tempdir
from textwrap import indent
from typing import List, Optional
from xmlrpc.client import Boolean
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

  # creates a new user in elasticsearch
  async def create_user(self, username: str, password: str, role: str, location: str) -> Boolean:
    query = {
      "username": username,
      "password": password,
      "role": role,
      "location": location
    }
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/users/_doc/{username}'
        response = await client.post(URI, headers=self.headers, json=query)
        return True
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

  # checks that the correct password has been supplied for a particular user
  async def auth_user(self, username: str, password: str):
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/users/_doc/{username}'
        response = await client.get(URI, headers=self.headers)
        if response.json()['found']:
          if response.json()['_source']['password'] == password:
            return response.json()['_source']
        return None
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)
        return None

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

  async def send_access_request(self, username, document_id, reason):
    notification = {
      "receiver": "admin",
      "sender": username,
      "type": "access_request",
      "document_id": document_id,
      "reason": reason,
      "resolved": False
    }
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/notifications/_doc'
        response = await client.post(URI, headers=self.headers, json=notification)
      # TODO: handle errors
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

  async def notify_of_access_grant(self, username, document_id):
    notification = {
      "receiver": username,
      "sender": "admin",
      "type": "access_grant",
      "document_id": document_id,
      "resolved": False
    }
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/notifications/_doc'
        response = await client.post(URI, headers=self.headers, json=notification)
      # TODO: handle errors
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

  async def get_notifications(self, username, user_type):
    query = {
      "query": {
        "bool": {
          "should": [
            {"match": {"receiver": username}},
            {"match": {"receiver": user_type}}
          ]
        }
      }
    }
    async with httpx.AsyncClient() as client:
      try:
        URI = f'{settings.ES_API}/notifications/_search'
        response = await client.post(URI, headers=self.headers, json=query)
        results = response.json()['hits']['hits']
        messages = []
        for r in results:
          message = r['_source'].copy()
          message['id'] = r['_id']
          messages.append(message)
        return messages
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

  async def grant_user_access_to_document(self, user_id, document_id):
    update = {
      "script" : {
          "source": "ctx._source.permitted_viewers.add(params.viewer)",
          "lang": "painless",
          "params" : {
              "viewer" : user_id
          }
      }
    }
    URI = f'{settings.ES_API}/{settings.DOC_INDEX}/_update'
    async with httpx.AsyncClient() as client:
      try:
        response = await client.post(URI, headers=self.headers, json=update)
      except Exception as err:
        print("***** Error in sending the request *****")
        print(err)

elasticSearch = ElasticSearch()