from unittest import result
from pydantic import BaseModel
import json

# Define the Tag class
class Tag(BaseModel):
  id: str
  name: str
  type: str
  

# Read Fake Json data
with open("./controllers/fake_data.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

tags = [Tag(**tag) for tag in jsonObject['tags']]

# Create Tag Controller class
class TagController: 

  def get_from_substring(self, substr: str): 
    tag_retrieved = [tag for tag in tags if substr.lower() in tag.name.lower()]
    return sorted(tag_retrieved, key=lambda tag: tag.name)

  def get_from_ids(self, ids: str): 
    return [tag for tag in tags if tag.id in ids]


controller = TagController()

