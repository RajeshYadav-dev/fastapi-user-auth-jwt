from fastapi import APIRouter,status,Depends
from src.student.schemas import StudentGetModel,StudentCreateModel,StudentUpdateModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.student.services import StudentServices
from src.database.main import get_async_session
from typing import List
from fastapi import HTTPException
from src.auth.dependencies import AccessTokenBearer

student_router = APIRouter()
student_service = StudentServices()
access_token_bearer = AccessTokenBearer()


@student_router.get("/",status_code=status.HTTP_200_OK,response_model=List[StudentGetModel])
async def get_all_students(
  session:AsyncSession=Depends(get_async_session),
  user_detail=Depends(access_token_bearer)
  ):
  try:
    students = await student_service.get_all_students_ser(session)
    return students
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  

@student_router.post("/",status_code=status.HTTP_201_CREATED,response_model=StudentGetModel)
async def create_a_student(
  student_data:StudentCreateModel,
  session:AsyncSession=Depends(get_async_session),
  user_detail=Depends(access_token_bearer)
  )->dict:
  try:
    student = await student_service.create_a_student_ser(student_data,session)
    return student
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@student_router.get("/{student_uid}",status_code=status.HTTP_200_OK,response_model=StudentGetModel)
async def get_a_student(
  student_uid:str,
  session:AsyncSession=Depends(get_async_session),
  user_detail=Depends(access_token_bearer)
  )->dict:
  student = await student_service.get_a_student_ser(student_uid,session)
  if student is None:
    # Raise a 404 error if no student is found
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
  return student  

@student_router.put("/{student_uid}",status_code=status.HTTP_200_OK,response_model=StudentGetModel)
async def update_a_student(
  student_uid:str,
  student_data:StudentUpdateModel,
  session:AsyncSession=Depends(get_async_session),
  user_detail=Depends(access_token_bearer)
  )->dict:
  try:
    updated_student = await student_service.update_a_student_ser(student_uid,student_data,session)
    return updated_student
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
  
  
@student_router.delete("/{student_id}")
async def delete_a_student(
  student_uid:str,
  session:AsyncSession=Depends(get_async_session),
  user_detail=Depends(access_token_bearer)
  )->dict:
  try:
    message = await student_service.delete_a_student_ser(student_uid,session)
    return message
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

