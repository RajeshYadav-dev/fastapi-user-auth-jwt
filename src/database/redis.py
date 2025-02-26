import redis.asyncio as aioredis
from src.config import Config


JTI_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
  host=Config.REDIS_HOST,
  port=Config.REDIS_PORT,
  db=0
)

async def add_jti_to_blocklist(jti:str)->None:
  await token_blocklist.set(
    name=jti,
    value="",
    ex=JTI_EXPIRY
  )
  
async def jti_token_in_blocklsit(jti:str)->bool: 
  _jti = await token_blocklist.get(jti)
  return _jti is not None
