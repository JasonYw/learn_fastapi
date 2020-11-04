from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app =FastAPI()


oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/token")
print('oauth2_scheme',oauth2_scheme)


class User(BaseModel):
    username:str
    e