from fastapi import APIRouter,Depends,status
from src.auth.schemas import UserCreateModel,UserModel,UserLoginModel
from src.auth.services import UserServices
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.database.main import get_async_session
from fastapi.exceptions import HTTPException
from src.auth.utils import create_access_token,decode_token,verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
service = UserServices()

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post('/signup',status_code=status.HTTP_201_CREATED,response_model=UserModel)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession=Depends(get_async_session)):
  email = user_data.email
  user_exists = await service.user_exists(email,session)
  
  if user_exists:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User already exits with this email.")
  
  new_user = await service.create_user(user_data,session)
  return new_user

@auth_router.post("/login")
async def login_users(login_data:UserLoginModel,session:AsyncSession=Depends(get_async_session)):
  email = login_data.email
  password = login_data.password
  
  user = await service.get_user_by_email(email,session)
  
  if user is not None:
    password_valid=verify_password(password,user.password_hash)
    if password_valid:
      access_token = create_access_token(
        user_data={
          'email':user.email,
          'user_uid':str(user.uid)
        }
        )
      refresh_token = create_access_token(
        user_data={
          'email':user.email,
          'user_uid':str(user.uid)
        },
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
        )
      
      return JSONResponse(
        content={
          "message":"Login Successfully",
          "access_token":access_token,
          "refresh_token":refresh_token,
          "user":{
            "email":user.email,
            "uid":str(user.uid)
          }
        }
      )
      
  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Email Or Password")    