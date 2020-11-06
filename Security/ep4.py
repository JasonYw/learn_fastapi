from datetime import datetime,timedelta
import jwt
from fastapi import Denpends,FastAPI,HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel


SECURET_KEY ="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =30


fake_user_db ={
    "root":{
        "username":"root",
        "email":"root@root.com",
        "hashed_password":"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled":False
    }
}

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    usernmae:str=None

class User(BaseModel):
    username:str
    email:str =None
    disabled:bool =None

class UserInDB(User):
    hashed_password:str

pwd_context =CryptContext(schemes=["bcrypt"])
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/token")
app =FastAPI()

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db,username:str):
    user_dict =db.get(username,None)
    if user_dict != None:
        return UserInDB(**user_dict)

def authenticate_user(fake_db,username:str,password:str):
    user =get_user(fake_db,username)
    if not user or not verify_password(password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def create_access_token(*,data:dict,expires_data:timedelta =None):
    to_encode =data.copy()
    expire =datetime.utcnow() +expires_data
    to_encode.update({"exp":expire})
    enoded_jwt =jwt.encode(to_encode,SECURET_KEY,algorithm=ALGORITHM)
    print(enoded_jwt)
    return enoded_jwt

async def get_current_user(token:str =Denpends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload =jwt.decode(token,SECURET_KEY,algorithms=[ALGORITHM])
        username:str =payload.get("sub")
        