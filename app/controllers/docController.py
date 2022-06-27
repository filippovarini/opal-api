from assets.document import Document, DocumentFields
from typing import List
from db.db_controller import database, SearchQuery, query_to_elastic_query


# Checks whether BIG list has all elements of SMALL
def isSublist(small: list, big: list) -> bool:
  return all(elem in big for elem in small)

# Controller to perform the Client's documentsearch
class DocumentController:

  # Searches the document from metadata stored in our DB (tags, fiels)
  async def get_from_metadata(self, tags: List[str], fields: DocumentFields) -> List[Document]:
    documents = await database.get_from_meta(tags, fields)
    return documents

  # Searches the document based on keywrods. Need to access the document text
  def get_from_keywords(self, keywords: List[str]) -> List[Document]:
    return []

  async def get_from_search_query(self, search_query: SearchQuery):
    return await database.get_from_search_query(query_to_elastic_query(search_query))
  
documentController = DocumentController()