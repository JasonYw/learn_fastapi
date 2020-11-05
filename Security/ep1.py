from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel,EmailStr

app =FastAPI()

#token 请求头为Authorization 值为Bearer + .....
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/token")
print('oauth2_scheme',oauth2_scheme)


class User(BaseModel):
    username:str
    password:str =None
    email:EmailStr =None
    full_name:str =None

def fake_decode_token(token):
    return User(
        username =token +"fakedecoded",email="john@example.com",full_name="john doe"
    )

async def get_current_user(token:str =Depends(oauth2_scheme)):
    print('token',token)
    return fake_decode_token(token)

@app.get("/users/me") #headers ={"Authorization":"Bearer rico"}
async def read_users_me(current_user:User =Depends(get_current_user)):
    return current_user

