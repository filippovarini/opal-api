from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

# Format of the document.
class DocumentFormat(str, Enum):
  PDF = 'PDF'
  WORD = 'WORD'
  HTML = 'HTML'
  

class Document(BaseModel):
  id: str
  format: DocumentFormat
  tags: Optional[List[str]]
  title: Optional[str]
  language: Optional[str]
  type: Optional[str]
  date: Optional[str]
  governing_law: Optional[List[str]]
  access: Optional[str]
  parties: Optional[List[str]]
  judges: Optional[List[str]]
  full_text: Optional[str]
  pdf_url: Optional[str]
  summary: Optional[str]
