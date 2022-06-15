from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

# Format of the document.
class DocumentFormat(str, Enum):
  PDF = 'PDF'
  WORD = 'WORD'
  HTML = 'HTML'

# Document source. Database where the document comes from.
class SourceDB(str, Enum):
  SEC = 'SEC'

class DocumentFields(BaseModel):
  title: Optional[str]
  language: Optional[str]
  type: Optional[str]
  topic: Optional[str]
  source: Optional[str]
  date: Optional[str]
  govlaw: Optional[str]
  access: Optional[str]
  status: Optional[str]

class Document(BaseModel):
  id: str
  format: DocumentFormat
  source: SourceDB
  tags: List[str]
  fields: DocumentFields
