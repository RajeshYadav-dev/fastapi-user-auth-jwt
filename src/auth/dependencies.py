from fastapi.security import HTTPBearer
from fastapi import Request
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException
from fastapi import status
from src.database.redis import jti_token_in_blocklsit

class TokenBearer(HTTPBearer):
  def __init__(self,auto_error = True):
    super().__init__(auto_error=auto_error)
    
  async def __call__(self, request:Request)->HTTPAuthorizationCredentials|None:
    cred = await super().__call__(request)  
    token = cred.credentials
    token_data = decode_token(token)
    
    if not self.validat_token(token):
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
          "error":"This token is invalid or expired.",
          "resolution":"Please get new token."
        }
      )
    if await jti_token_in_blocklsit(token_data):
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
          "error":"This token is invalid or revoked.",
          "resolution":"Please get new token."
        }
      )
    self.verify_token_data(token_data)
    return token_data
  
  def validat_token(self,token:str)->bool:
    token_data = decode_token(token)
    return token_data is not None
  
  def verify_token_data(self,token_data):
    raise NotImplementedError("Please override this method in child classes.")
    
    
    
class AccessTokenBearer(TokenBearer):
  def verify_token_data(self,token_data)->None:
    if token_data and token_data["refresh"]:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Please provide a valid access token."
      )

class RefreshTokenBearer(TokenBearer):
  def verify_token_data(self,token_data)->None:
    if token_data and not token_data["refresh"]:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Please provide a fresh access token."
      )   
    