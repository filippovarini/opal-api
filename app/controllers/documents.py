from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum

class Fields(BaseModel):
  title: Optional[str]
  language: Optional[str]

class UserSearch(BaseModel):
  tags: Optional[List[str]] = []
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

# Controller to perform the Client's documentsearch
class Document:

  # Searches the document from metadata stored in our DB (tags, fiels)
  def get_from_metadata(self, tags: List[str], fields: Fields) -> List[Document]:
    return f'getting documents for tags ${tags} and fields ${fields}'

  # Searches the document based on keywrods. Need to access the document text
  def get_from_keywords(self, keywords: List[str]) -> List[Document]:
    return f'getting documents for keywords: ${keywords}'

  
documentController = Document()