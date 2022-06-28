from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Response, status, Request
from controllers.tagController import controller
from controllers.userController import userController

router = APIRouter()

# Type model of User Search request body
class UserDetails(BaseModel):
  role: Optional[str] = "intern"  
  location: Optional[str] = "global"

@router.get("/auth")
async def tags_from_substring(request: Request, response: Response):
  username = request.headers.get('username')
  password = request.headers.get('password')
  auth_status = False
  if username is not None and password is not None:
    # check if username and password is correct
    if not await userController.auth_user(username, password):
      response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        auth_status = True

  return {"authenticated": auth_status}

@router.post("/create")
async def tags_from_id(request: Request, user_details: UserDetails):
	username = request.headers.get('username')
	password = request.headers.get('password')
	if username is None or password is None:
		return {"created": False}
	await userController.create_user(username, password, user_details.role, user_details.location)
	return {"created": True}