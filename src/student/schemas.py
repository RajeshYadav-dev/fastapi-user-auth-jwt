from pydantic import BaseModel
import uuid
from datetime import datetime

class StudentGetModel(BaseModel):
  uid : uuid.UUID
  first_name : str
  last_name : str
  email : str
  age : int
  city : str
  standard : int
  created_at: datetime
  updated_at: datetime
  
class StudentCreateModel(BaseModel):
  first_name : str
  last_name : str
  email : str
  age : int
  city : str
  standard : int 
  
class StudentUpdateModel(BaseModel):
  first_name : str
  last_name : str
  email : str
  age : int
  city : str
  standard : int
  updated_at: datetime   