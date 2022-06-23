from typing import List, Dict
from fastapi import APIRouter, Response, status, Request
from controllers.tagController import controller
from controllers.userController import userController

router = APIRouter()

@router.get("/auth")
def tags_from_substring(request: Request, response: Response):
  username = request.headers.get('username')
  password = request.headers.get('password')
  auth_status = False
  if username is not None and password is not None:
    # check if username and password is correct
    if not userController.auth_user(username, password):
      response.status_code = status.HTTP_401_UNAUTHORIZED
    else:
        auth_status = True

  return {"authenticated": auth_status}

@router.post("/create")
def tags_from_id(request: Request):
	username = request.headers.get('username')
	password = request.headers.get('password')
	if username is None or password is None:
		return {"created": False}
	userController.create_user(username, password)
	return {"created": True}