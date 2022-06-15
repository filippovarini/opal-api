from pydantic import BaseModel
from typing import List, Optional

class Fields(BaseModel):
  title: Optional[str]
  language: Optional[str]

class UserSearch(BaseModel):
  tags: Optional[List[str]] = []       # list of tag ids
  keywords: Optional[List[str]] = []
  fields: Optional[Fields] = {}