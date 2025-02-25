from pydantic import BaseModel,Field
from datetime import datetime

class UserCreateModel(BaseModel):
  first_name:str
  last_name:str
  username :str = Field(max_length=10)
  email:str = Field(max_length=50)
  password:str = Field(min_length=8)
  
class UserModel(BaseModel):
  uid:str
  username:str
  email:str
  first_name:str
  last_name:str
  is_verified:bool=False
  password_hash :str 
  created_at: datetime 
  updated_at: datetime 
  
class UserLoginModel(BaseModel):
  email:str = Field(max_length=50)
  password:str = Field(min_length=8)
  