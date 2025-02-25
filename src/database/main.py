from sqlmodel import SQLModel,create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker


# 1. Creating the Async Engine
'''
Config.DATABASE_URL — Your database connection string (like mysql+asyncmy://user:pass@localhost/dbname).
create_engine() — Normally used for synchronous engines, but here it’s wrapped with AsyncEngine for async support.
echo=True — Enables SQL query logging (useful for debugging!).

Why the AsyncEngine wrapper?

create_engine() produces a synchronous engine.
AsyncEngine adapts it for async/await usage (so your DB operations don’t block your app).
'''
async_engine = AsyncEngine(
  create_engine(
    url=Config.DATABASE_URL,
    echo=True
  )
)

# 2. Database Initialization
'''
async with async_engine.begin() — Opens an async connection for executing SQL commands.
from src.student.models import StudentSQLModel — Import your models so SQLModel knows what tables to create.
await con.run_sync(SQLModel.metadata.create_all) — Runs the CREATE TABLE statements (sync method executed in an async way).
Why run_sync?
Some SQLAlchemy methods are still synchronous (like schema generation), so run_sync bridges the gap between sync and async worlds.'''
async def init_database():
  async with async_engine.begin() as con:
    from src.student.models import StudentSqlModel
    await con.run_sync(SQLModel.metadata.create_all)
    
# 3. Session Factory
'''
sessionmaker() — A factory to create new database sessions.
bind=async_engine — Tells sessions to use your async database engine.
class_=AsyncSession — Uses async sessions instead of the default sync ones.
expire_on_commit=False — Prevents SQLAlchemy from automatically expiring objects after a commit (useful for async workflows).
'''
async def get_async_session()->AsyncSession:
  Session = sessionmaker(
    bind=async_engine,
    class_= AsyncSession,
    expire_on_commit=False
  )   
  
  # 4. Dependency Injection for FastAPI
  '''
  async with Session() — Opens a new async database session.
  yield session — Returns the session to FastAPI’s dependency injection system (so each request can get its own session).
  Session closes automatically when the request is done, thanks to the async with block.
  '''
  async with Session() as session:
    yield session
    