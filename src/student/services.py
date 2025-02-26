from sqlalchemy.ext.asyncio.session import AsyncSession
from src.student.models import StudentSqlModel
from sqlmodel import select,desc
from sqlalchemy.exc import SQLAlchemyError
from src.student.schemas import StudentCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status

class StudentServices:
  try:
    # Define an async method to get all students, using a database session (AsyncSession)
    async def get_all_students_ser(self, session: AsyncSession):
      # Create a SQL statement to select all rows from the StudentSqlModel table,
      # ordering them by the 'created_at' column in descending order (newest first)
      statement = select(StudentSqlModel).order_by(desc(StudentSqlModel.created_at))

      # Execute the SQL query asynchronously using the provided session.
      # 'execute()' runs the query and returns a result object containing rows.
      result = await session.execute(statement)
      
      # Fetch all rows from the result. 
      # 'result.all()' returns a list of rows, but each row is a tuple containing the model instance.
       # Get only the model instances (not tuples)
      students = result.scalars().all()
      return students
  except SQLAlchemyError as e:
    # Raise a generic error message for the user
    raise Exception("An error occurred while fetching students. Please try again later.")
  
  async def get_student_by_email(self,email:str,session:AsyncSession):
    try:
      statement = select(StudentSqlModel).where(StudentSqlModel.email==email)
      result = await session.execute(statement)
      user = result.scalars().first()
      return True if user is not None else False
    except SQLAlchemyError as e:
    # Raise a generic error message for the user
     raise Exception("An error occurred while fetching students. Please try again later.")

  async def create_a_student_ser(self,student_data:StudentCreateModel,session:AsyncSession):
    try:
      if await self.get_student_by_email(student_data.email,session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Already present with Email: {student_data.email}")
      
      student_data_dict = student_data.model_dump()
      new_student =  StudentSqlModel(**student_data_dict)
      
      session.add(new_student)
      await session.commit()
      await session.refresh(new_student)
      return new_student
    except SQLAlchemyError as e:
      # Raise a generic error message for the user
      raise Exception("An error occurred while creating students. Please try again later.")
   


  async def get_a_student_ser(self,student_uid:str,session:AsyncSession):
   try:
      statement = select(StudentSqlModel).where(StudentSqlModel.uid==student_uid)
      result = await session.execute(statement)
      user = result.scalars().first()
      print("User",user)
      return user
   except SQLAlchemyError as e:
    # Raise a generic error message for the user
    raise Exception("An error occurred while fetching students. Please try again later.")


  async def update_a_student_ser(self,student_uid:str,student_data:StudentSqlModel,session:AsyncSession):
    try:
      student_to_update = await self.get_a_student_ser(student_uid,session)
      if student_to_update:
        student_data_dict = student_data.model_dump()
        for k,v in student_data_dict.items():
          setattr(student_to_update,k,v)
        await session.commit()
        await session.refresh(student_to_update)  
        return student_to_update
      else:
        raise Exception(f"No Student found with uid:{student_uid}")
    except SQLAlchemyError as e:
      # Raise a generic error message for the user
      raise Exception("An error occurred while fetching students. Please try again later.")



  async def delete_a_student_ser(self,student_uid:str,session:AsyncSession):
    try:
      student_to_delete = await self.get_a_student_ser(student_uid,session)
      if student_to_delete:
        await session.delete(student_to_delete)
        await session.commit()
        return {"message:":"Student deleted successfully"}
      else:
        raise Exception(f"No Student found with uid:{student_uid}")
    except SQLAlchemyError as e:
      # Raise a generic error message for the user
      raise Exception("An error occurred while fetching students. Please try again later.")