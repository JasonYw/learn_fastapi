from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import Boolean,Column,Integer,String

app =FastAPI()

SQLALCHEMY_DATABASES_URL ="mysql+pymysql://root:0125@localhost:3306/Fastapi"


engine = create_engine(SQLALCHEMY_DATABASES_URL)


SessionLocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base =declarative_base()

class ORM_EP0_USER(Base):
    __tablename__ ="orm_ep0_user"

    id =Column(Integer,primary_key=True,index=True)
    email =Column(String(50),unique=True,index=True)
    hashed_password =Column(String(50))
    is_cative =Column(Boolean,default=True)


class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    passwprd:str

class User(UserBase):
    id:int
    is_active:bool
    class Config:
        orm_mode =True

Base.metadata.create_all(bind=engine) #创建orm_ep0_user 表还有数据库


def get_db():
    try:
        db =SessionLocal()
        yield db
    finally:
        db.close()
        print("数据库关闭")
    
def get_user(db:Session,user_id:int):
    CCC =db.query(ORM_EP0_USER).filter(ORM_EP0_USER.id == user_id).first()
    print('ccc:',CCC)
    return CCC

if __name__ == "__main__":
    for i in get_db():
        c =get_user(db=i,user_id=1)
        print(c)