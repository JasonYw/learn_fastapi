from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from getpass import getuser

if getuser() == "rico":
    SQL_URL ="mysql+pymysql:root:rico0125@localhost:3306/Fastapi"
else:
    SQL_URL ="mysql+pymysql://root:0125@localhost:3306/Fastapi"

engine =create_engine(SQL_URL)

SessionLocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base =declarative_base()

