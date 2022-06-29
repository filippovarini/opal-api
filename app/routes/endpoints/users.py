from typing import List, Dict, Optional
from fastapi import APIRouter, Response, status, Request
from controllers.tagController import controller
from controllers.userController import userController
from assets.user import UserDetails

router = APIRouter()

@router.get("/auth")
async def auth_user(request: Request, response: Response):
  user = await userController.auth_user_with_request(request)
  if user is None:
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"authenticated": False}
  else:
    return {"authenticated": True, "user": user}

@router.post("/create")
async def create_user(request: Request, user_details: UserDetails):
	username = request.headers.get('username')
	password = request.headers.get('password')
	if username is None or password is None:
		return {"created": False}
	await userController.create_user(username, password, user_details.role, user_details.location)
	return {"created": True}

@router.get("/notifications")
async def notifications(request: Request):
  user = await userController.auth_user_with_request(request)
  notifications = await userController.get_notifications(user['username'], user.get('role', 'intern'))
  return {
    "notifications": notifications
  }