from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import pymysql as sql
from pymysql.cursors import DictCursor

Base=declarative_base()

class Settings(BaseSettings):
    API_PREFIX:str="/api"
    HOST:str=''
    PASSWORD:str=''
    DB_USER:str=''
    DB_PORT:str=''
    
    ALLOWED_ORIGINS:str=''
    
    DEBUG:bool=False
    
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls,v:str) -> List[str]:
        return v.split(',') if v else []
    
    class Config:
        env_file=".env"
        env_file_encoding="utf-8"
        case_sensitive=True
        
settings=Settings()

def create_database(database:str):
    conn=sql.connect(
        host=settings.HOST,
        user=settings.DB_USER,
        passwd=settings.PASSWORD,
        charset="utf8mb4"
    )
    cursor=conn.cursor()
    query=f'''create database if not exists {database}'''
    cursor.execute(query)
    
    conn.close()

project_database="employee_management_system"
create_database(project_database)

engine=create_engine(f"mysql+pymysql://{settings.DB_USER}:{settings.PASSWORD.replace('@','%40')}@{settings.HOST}:{settings.DB_PORT}/{project_database}")

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally :
        db.close()
        
def get_raw_db():
    db=engine.raw_connection()
    try:
        yield db
    finally:
        db.close()
        
def create_table():
    Base.metadata.create_all(bind=engine)
