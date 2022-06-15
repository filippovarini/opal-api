from assets.document import Document, DocumentFields
from typing import List
import json

# Read Fake Json data
with open("./controllers/fake_data.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()


documents = [Document(**doc) for doc in jsonObject['documents']]

# Controller to perform the Client's documentsearch
class DocumentController:

  # Searches the document from metadata stored in our DB (tags, fiels)
  def get_from_metadata(self, tags: List[str], fields: DocumentFields) -> List[Document]:
    # Checks whether BIG list has all elements of SMALL
    def isSublist(small: list, big: list) -> bool:
      return all(elem in big for elem in small)
  
    return [doc for doc in documents if isSublist(tags, doc.tags)]

  # Searches the document based on keywrods. Need to access the document text
  def get_from_keywords(self, keywords: List[str]) -> List[Document]:
    return []

  
documentController = DocumentController()