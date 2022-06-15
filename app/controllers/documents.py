from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum
import json

with open("./controllers/fake_data.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

class Fields(BaseModel):
  title: Optional[str]
  language: Optional[str]

class UserSearch(BaseModel):
  tags: Optional[List[str]] = []       # list of tag ids
  keywords: Optional[List[str]] = []
  fields: Optional[Fields] = {}

# Format of the document.
class DocumentFormat(Enum):
  PDF = 0
  WORD = 1
  HTML = 2

# Document source. Database where the document comes from.
class SourceDB(Enum):
  SEC = 0

class Document(BaseModel):
  id: str
  format: DocumentFormat
  source_db: SourceDB


documents = jsonObject['documents']

# Controller to perform the Client's documentsearch
class Document:

  # Searches the document from metadata stored in our DB (tags, fiels)
  def get_from_metadata(self, tags: List[str], fields: Fields) -> List[Document]:
    # Checks whether BIG list has all elements of SMALL
    def isSublist(small: list, big: list) -> bool:
      return all(elem in big for elem in small)
  
    return [doc for doc in documents if isSublist(tags, doc['tags'])]

  # Searches the document based on keywrods. Need to access the document text
  def get_from_keywords(self, keywords: List[str]) -> List[Document]:
    return []

  
documentController = Document()