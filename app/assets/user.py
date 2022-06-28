from pydantic import BaseModel
from typing import Optional

# Type model of User Search request body
class UserDetails(BaseModel):
  role: Optional[str] = "intern"  
  location: Optional[str] = "global"

# Full type model of a user
class User(UserDetails):
    username: str
    password: str