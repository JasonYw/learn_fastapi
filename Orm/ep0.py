from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import Boolean,Column,Integer,String
from getpass import getuser

app =FastAPI()
if getuser() =="rico":
    SQLALCHEMY_DATABASES_URL ="mysql+pymysql://root:rico0125@localhost:3306/Fastapi"
else:
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

def get_user_info(db:Session,user_email:str):
    userinfo =db.query(ORM_EP0_USER).filter(ORM_EP0_USER.email ==user_email).first()
    userinfo_dict ={
        "id":userinfo.id,
        "email":userinfo.email,
        "is_active":userinfo.is_cative,
        "password":userinfo.hashed_password
    }
    return userinfo_dict

def db_create_user(db:Session,user:UserCreate):
    fake_hashed_password =user.passwprd + "notreallyhashed"
    db_user =ORM_EP0_USER(email=user.email,hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/users/",response_model=User)
def create_user(user:UserCreate,db:Session =Depends(get_db)):
    try:
        db_create_user(db=db,user=user)
        return get_user_info(db=db,user_email=user.email)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,detail="can‘t insert userdata")
    

@app.get("/users/{user_id}",response_model=User)
def read_user(user_id:int,db:Session=Depends(get_db)):
    db_user =get_user(db,user_id=user_id)
    print(db_user)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return get_user_info(db=db,user_email=db_user.email)

if __name__ == "__main__":
    for i in get_db():
        c =get_user_info(db=i,user_email="root@root.com")
        print(c.id)