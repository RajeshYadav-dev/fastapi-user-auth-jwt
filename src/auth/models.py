from sqlmodel import SQLModel,Field,Column
from datetime import datetime
import sqlalchemy.dialects.mysql as my
import uuid

class User(SQLModel,table=True):
  __tablename__ = "user"
  uid:str = Field(sa_column=Column(
    my.CHAR(36),
    nullable=False,
    primary_key=True,
    default=lambda:str(uuid.uuid4())
  ))
  username:str
  email:str
  first_name:str
  last_name:str
  is_verified:bool=False
  password_hash :str = Field(exclude=True)
  created_at: datetime = Field(sa_column=Column(my.TIMESTAMP,default=datetime.now))
  updated_at: datetime = Field(sa_column=Column(my.TIMESTAMP,default=datetime.now,onupdate=datetime.now))
  
  def __repr__(self):
    return f"<User:{self.username}>"
  
 