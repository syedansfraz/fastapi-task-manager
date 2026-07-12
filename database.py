from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://taskadmin:devpassword@localhost:5432/taskdb"
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "tasks"
    id       = Column(Integer, primary_key=True, index=True)
    title    = Column(String, nullable=False)
    deadline = Column(String, nullable=False)
    done     = Column(Boolean, default=False)
    priority = Column(String, default="medium")

def init_db():
    Base.metadata.create_all(bind=engine)