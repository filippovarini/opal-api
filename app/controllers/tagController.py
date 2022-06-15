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
    return [tag for tag in tags if substr.lower() in tag.name.lower()]


controller = TagController()

