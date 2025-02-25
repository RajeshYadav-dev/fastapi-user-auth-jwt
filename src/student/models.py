from sqlmodel import SQLModel,Field,Column
from datetime import datetime
import sqlalchemy.dialects.mysql as my
import uuid


class StudentSqlModel(SQLModel,table=True):
  __tablename__ = "students"
  uid : str = Field(sa_column=Column(
    my.CHAR(36),
    nullable=False,
    primary_key=True,
    default=lambda:str(uuid.uuid4())
  ))
  first_name : str
  last_name : str
  email : str
  age : int
  city : str
  standard : int
  created_at: datetime = Field(sa_column=Column(my.TIMESTAMP,default=datetime.now))
  updated_at: datetime = Field(sa_column=Column(my.TIMESTAMP,default=datetime.now,onupdate=datetime.now))
  
  def __repr__(self):
    return f"<Student:{self.first_name}>"