from pydantic import BaseModel
from db.db_controller import database
import json

# Define the Tag class
class User(BaseModel):
  id: str
  username: str
  password: str

# Create Tag Controller class
class UserController: 

  def auth_user(self, username: str, password: str): 
    return database.auth_user(username, password)

  def create_user(self, username: str, password: str):
    database.create_user(username, password)
    return True


userController = UserController()