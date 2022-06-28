from fastapi import Request
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

  async def auth_user_with_request(self, request: Request):
    username = request.headers.get('username')
    password = request.headers.get('password')
    if username is not None and password is not None:
      # check if username and password is correct
      return await userController.auth_user(username, password)
    return None

  async def auth_user(self, username: str, password: str): 
    return await database.auth_user(username, password)

  async def create_user(self, username: str, password: str, role: str, location: str):
    await database.create_user(username, password, role, location)
    return True

  async def request_document_access(self, username, document_id, reason):
    await database.send_access_request(username, document_id, reason)

  async def notify_of_access_grant(self, username, document_id):
    await database.notify_of_access_grant(username, document_id)

  async def get_notifications(self, username, user_type):
    return await database.get_notifications(username, user_type)


userController = UserController()