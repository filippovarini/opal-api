from typing import List, Dict, Optional
from unittest import result
from pydantic import BaseModel
from db.db_controller import database
import json

# Define the Tag class
class Tag(BaseModel):
  id: str
  name: str
  owner: Optional[str] = "global"
  type: Optional[str] = "user_defined"
  

# Read Fake Json data
with open("./controllers/fake_data.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

tags = [Tag(**tag) for tag in jsonObject['tags']]

# Create Tag Controller class
class TagController: 

  async def get_from_substring(self, substr: str, username: str = None, category: str = None): 
    if category is None:
      tag_retrieved = [tag for tag in tags if substr.lower() in tag.name.lower()]
      user_tags = await database.suggest_user_search_tags(substr)
      tag_retrieved = tag_retrieved + [Tag(**tag) for tag in user_tags]
      return sorted(tag_retrieved, key=lambda tag: tag.name)
    else:
      await database.suggest_tags_for_category(substr, category)

  def get_from_ids(self, ids: str): 
    return [tag for tag in tags if tag.id in ids]

  async def add_search_tag(self, username: str, tag_name: str, result_ids: List[str], search):
    await database.add_user_search_tag(username, tag_name, result_ids, search)


controller = TagController()

