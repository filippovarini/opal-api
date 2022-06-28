from typing import List, Dict, Optional
from fastapi import APIRouter, Response, status, Request
from controllers.tagController import controller
from controllers.userController import userController
from assets.user import UserDetails

router = APIRouter()

@router.get("/auth")
async def tags_from_substring(request: Request, response: Response):
  user = await userController.auth_user_with_request(request)
  auth_status = False
  if user is None:
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