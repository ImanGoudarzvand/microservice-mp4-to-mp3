from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
import os 

# POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
# POSTGRES_HOST = os.environ["POSTGRES_HOST"]
# POSTGRES_PORT = os.environ["POSTGRES_PORT"]
# POSTGRES_DATABASE = os.environ["POSTGRES_DATABASE"]


# DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
DATABASE_URL = f"postgresql://postgres:pass@0.0.0.0:5432/postgres"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")