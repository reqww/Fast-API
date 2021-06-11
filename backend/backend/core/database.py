from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pass@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
