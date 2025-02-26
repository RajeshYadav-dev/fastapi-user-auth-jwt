from fastapi import APIRouter,Depends,status
from src.auth.schemas import UserCreateModel,UserModel,UserLoginModel
from src.auth.services import UserServices
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.database.main import get_async_session
from fastapi.exceptions import HTTPException
from src.auth.utils import create_access_token,verify_password
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer,AccessTokenBearer
from src.database.redis import add_jti_to_blocklist,jti_token_in_blocklsit

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

@auth_router.get('/refresh-token')
async def get_refresh_token(token_detail:dict=Depends(RefreshTokenBearer())):
  expiry_timestamp = token_detail['exp']
  
  if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
    new_access_token = create_access_token(user_data=token_detail["user"])
    return JSONResponse(
      content={
        "access_token":new_access_token
      }
    )
    
  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Or Expired Token ")  
  
@auth_router.get("/logout")  
async def revoked_token(token_detail:dict=Depends(AccessTokenBearer())):
  jti = token_detail['jti']
  await add_jti_to_blocklist(jti)
  return JSONResponse(content={
    "message":"Logout Successfully.",
    },
     status_code=status.HTTP_200_OK                 
    )