from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.student.router import student_router
from src.auth.router import auth_router
from src.database.main import init_database

@asynccontextmanager
async def life_span(app:FastAPI):
  print("**********SERVER IS STARTED**********")
  await init_database()
  yield
  print("**********SERVER HAS BEEN STOPPED**********")

version = "v1"
app = FastAPI(
  title="REST API",
  description="REST API for Student Review Web Service",
  version=version,
  lifespan=life_span
)

app.include_router(student_router,prefix=f"/api/{version}/students",tags=["student"])
app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=["auth"])