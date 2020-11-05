from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel
from typing import Optional
from datetime import datetime,timedelta
from passlib.context import CryptContext
from jwt import PyJWTError
app =FastAPI()

'''
几种安全机制
    OAuth2
    OpenID Connect
    OpenAPI
        -apikey
        -http
        -oauth2
        -openIdConnect

FastAPI通过引入fastapi.security模块，可以支持以上所有的安全机制，并且简化了使用方法

OAuth2PasswordBearer 是接收url作为参数的一个类，客户端会向该url发送username和password参数
然后得到一个token值
OAuth2PasswordBearer并不会创建相应的url路径操作，只是指明了客户端用来获取token的目标url
当请求到来的时候，FastAPI会检查请求的Authorization头信息，如果没有找到Authorization头信息，或者头信息
内容不是Bearer token，他会返回401状态码
通过pip install pyjwt 生成和校验jwt token
pip install python-multipart 因为OAuth2需要通过表单数据来发送username和password信息

模拟用户登陆过程
为了数据安全，利用PassLib 对入库的用户名密码进行加密处理，推荐的加密算法是“Bcrpt“ 我们需要安装依赖包
pip install passlib
pip install bcrypt
用户名密码->后端->用户信息校验，查询当前系统是否存在该用户，以及密码是否正确，存在则生成JWT toekn并返回，JWT payload可以携带自定义数据
'''           

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#模拟数据库数据
fake_users_db ={
    "tom":{
        "username":"tom",
        "email":"tom@tom.com",
        'hashed_password':"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled":False,
    }
}

class token(BaseModel):
    access_token:str
    token_type:str

class User(BaseModel):
    username:str
    email:str =None
    disabled:bool =None

pwd_context =CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/token")

def verify_password(plain_password,hashed_password):
    '''
        校验密码    
    '''
    return pwd_context.verify_password()

def get_password_hash(password):
    '''
        密码哈希
    '''
    return pwd_context.hash(password)

def get_user(db,username:str):
    '''
        模拟从数据库读取用户消息
    '''
    if username in db:
        user_dict =db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db,username:str,password:str):
    '''
        用户信息校验
    '''
    user =get_user(fake_db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    else:
        return user

def create_acess_token(data:dict,expires_dalta:timedelta =None):
    '''
        生成token，带有过期时间
    ''' 
    to_encode =data.copy()
    if expires_dalta:
        expire =datetime.utcnow() +expire_delta
    else:
        expire =datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt =jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM
    )
    return encoded_jwt

@app.post("/token",response_model =token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends()):
    '''
        校验用户信息
    '''
    user =authenticate_user(fake_users_db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers ={"WWW-Authenticate":"Bearer"}
        )
    '''
        生成并返回token信息
    '''
    access_token_expires =timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =create_acess_token(
        data={"sub":"test"},expires_dalta=access_token_expires
    )
    return {"access_token":access_token,"token_type":"bearer"}


#终端获取到token信息后，必须在后续请求的Authorization头信息中带有Bearer token,才能被允许访问
#添加校验函数，对请求合法性进行校验，读取到token内容解析并进行验证

async def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception =HTTPException(
        status_code =status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload =jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM
        ])
        username:str =payload.get("sub")
        if username == None:
            raise credentials_exception
        token_data =TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user =get_user(fake_users_db,username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/users/me/",response_model=User)
async def read_users_me(current_user:Depends(get_current_user)):
    return current_user