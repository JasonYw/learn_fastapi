from typing import List
from fastapi import Depends,FastAPI,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal,engine
import models,schemas
from crud import Operation_User,Operation_Item

models.Base.metadata,create_all(bind=engine)

app =FastAPI()

def get_db():
    try:
        db =SessionLocal()
        yield db
    finally:
        db.close()
        print('success closing db')


@app.get("/users/",response_model=List[schemas.User])
def read_users(skip:int =0,limit:int=100,db:Session =Depends(get_db)):
    users =Operation_User.get_user(db,skip=skip,limit=limit)
    return users

@app.post("/users/",response_model=List[schemas.User])
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    db_user =Operation_User.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="email already registered")
    return Operation_User.create_user(db=db,user=user)

