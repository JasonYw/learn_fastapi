from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel,EmailStr

app =FastAPI()

oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/token") #密码服务器的作用

fake_users_db={
    "root":{
        "username":"root",
        "fullname":"root",
        "email":"root@root.com",
        "hashed_password":"fakehashed0125",
        "disabled":False,
    },
    "rico":{
        "username":"rico",
        "fullname":"rico",
        "email":"rico@rico.com",
        "hashed_password":"fakehashed0125",
        "disabled":True,
    }
}

class User(BaseModel):
    username:str
    password:str =None
    email:EmailStr =None
    disabled: bool = None


class UserInDB(User):
    hashed_password:str
    username:str

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db,username:str):
    if username in db:
        user_dict =db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user =get_user(fake_users_db,token)
    return user

async def get_current_user(token:str =Depends(oauth2_scheme)):
    user =fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid UNAUTHORIZED',
            headers={"WWW-Authenticate":'Bearer'}
        )
    return user


async def get_current_active_user(current_user:User =Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=400,
            detail="baned"
        )
    return current_user

@app.post("/token")
async def login(form_data:OAuth2PasswordRequestForm =Depends()):
    #form_data:OAuth2PasswordRequestForm =Depends() 用户登陆的form
    print(form_data.__dict__)
    user_dict =fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail='Incorrect username'
        )
    user = UserInDB(**user_dict)
    hashed_password =fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="incorrect username or password"
        )
    return {"access_token":user.username,"token_type":"bearer"}

        
@app.get("/users/me")
async def read_users_me(current_user:User =Depends(get_current_active_user)):
    return current_user