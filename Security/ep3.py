# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, FastAPI, HTTPException # , status
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext # passlib 处理哈希加密的包
from pydantic import BaseModel

'''
a.session验证的方式
    1、用户向服务器发送用户名和密码。
    2、服务器验证通过后，在当前对话（session）里面保存相关数据，比如用户角色、登录时间等等。
    3、服务器向用户返回一个 session_id，写入用户的 Cookie。
    4、用户随后的每一次请求，都会通过 Cookie，将 session_id 传回服务器。
    5、服务器收到 session_id，找到前期保存的数据，由此得知用户的身份。
    缺点：
        这种模式的问题在于，扩展性（scaling）不好。单机当然没有问题，如果是服务器集群，或者是跨域的服务导向架构，就要求 session 数据共享，每台服务器都能够读取 session。
        举例来说，A 网站和 B 网站是同一家公司的关联服务。现在要求，用户只要在其中一个网站登录，再访问另一个网站就会自动登录，请问怎么实现？
        一种解决方案是 session 数据持久化，写入数据库或别的持久层。各种服务收到请求后，都向持久层请求数据。这种方案的优点是架构清晰，缺点是工程量比较大。另外，持久层万一挂了，就会单点失败。
        另一种方案是服务器索性不保存 session 数据了，所有数据都保存在客户端，每次请求都发回服务器。JWT 就是这种方案的一个代表。
b.jwt原理
    JWT 的原理是，服务器认证以后，生成一个 JSON 对象，发回给用户。
    用户与服务端通信的时候，都要发回这个 JSON 对象。服务器完全只靠这个对象认定用户身份。为了防止用户篡改数据，服务器在生成这个对象的时候，会加上签名（详见后文）。
    服务器就不保存任何 session 数据了，也就是说，服务器变成无状态了，从而比较容易实现扩展。
    jwt:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
        1.通过.分割
        2.Header(头部).Payload(负载).Signature(签名) -> header.Payload.Signature
        3.header
            {
                "alg": "HS256",
                "typ": "JWT"
            }
            上面代码中，alg属性表示签名的算法（algorithm），默认是 HMAC SHA256（写成 HS256）；
            typ属性表示这个令牌（token）的类型（type），JWT 令牌统一写为JWT。
            最后，将上面的 JSON 对象使用 Base64URL 算法（详见后文）转成字符串。
        4.Payload 
            JWT 规定了7个官方字段也就是key：
                iss (issuer)：签发人
                exp (expiration time)：过期时间
                sub (subject)：主题
                aud (audience)：受众
                nbf (Not Before)：生效时间
                iat (Issued At)：签发时间
                jti (JWT ID)：编号
            除了官方字段，你还可以在这个部分定义私有字段
            注意，Payload这部分数据默认是不加密的，任何人都可以读到，所以不要把秘密信息放在这个部分。
            这个 JSON 对象也要使用 Base64URL 算法转成字符串。
        5.Signature
            Signature 部分是对前两部分的签名，防止数据篡改。
                首先，需要指定一个密钥（secret）
                这个密钥只存储在服务器
                使用 Header 里面指定的签名算法（默认是 HMAC SHA256），按照下面的公式产生签名。
                HMACSHA256(
                    base64UrlEncode(header) + "." +
                    base64UrlEncode(payload),
                    secret
                )
        6.算出签名以后，把 Header、Payload、Signature 三个部分拼成一个字符串，每个部分之间用"点"（.）分隔，就可以返回给用户。
        7.使用方式：   
            客户端收到服务器返回的 JWT，可以储存在 Cookie 里面，也可以储存在 localStorage。
            客户端每次与服务器通信，都要带上这个 JWT。
            你可以把它放在 Cookie 里面自动发送，但是这样不能跨域，所以更好的做法是放在 HTTP 请求的头信息Authorization字段里面
            headers{"Authorization": "Bearer jwt"}
        8.特点：
            (1).JWT Payload 默认是不加密，但也是可以加密的。生成原始 Token 以后，可以用密钥再加密一次。
            (2).JWT Payload 不加密的情况下，不能将秘密数据写入 JWT。
            (3).JWT 不仅可以用于认证，也可以用于交换信息。有效使用 JWT，可以降低服务器查询数据库的次数。
            (4).JWT 的最大缺点是，由于服务器不保存 session 状态，因此无法在使用过程中废止某个 token，或者更改 token 的权限。也就是说，一旦 JWT 签发了，在到期之前就会始终有效，除非服务器部署额外的逻辑。
            (5).JWT 本身包含了认证信息，为了减少盗用，JWT 的有效期应该设置得比较短。对于一些比较重要的权限，使用时应该再次对用户进行认证。
            (5).为了减少盗用，JWT 不应该使用 HTTP 协议明码传输，要使用 HTTPS 协议传输。            
'''

# to get a string like this run: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"# 密钥
ALGORITHM = "HS256"     # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # 访问令牌过期分钟

# 用户数据（模拟）
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}



class Token(BaseModel):     # 令牌空壳
    access_token: str
    token_type: str
class TokenData(BaseModel): # 令牌数据
    username: str = None
class User(BaseModel):      # 用户基础模型
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None
class UserInDB(User):       # 用户输入数据模型
    hashed_password: str
    username: str           # 此行多余，为了vscode不报错而已。
# Context是上下文  CryptContext是密码上下文   schemes是计划     deprecated是不赞成（强烈反对）
# bcrypt是加密算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme是令牌对象，token: str = Depends(oauth2_scheme)后就是之前加密的令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app = FastAPI()



# verify_password验证密码   plain_password普通密码      hashed_password哈希密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
# 获取密码哈希
def get_password_hash(password):
    return pwd_context.hash(password)
# 获取用户
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
# 验证用户
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print('验证用户user :', user)
    print('验证用户type :', type(user))
    return user  # <class '__main__.UserInDB'>




# 创建访问令牌
def create_access_token(*,data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta # expire 令牌到期时间 
    to_encode.update({"exp": expire})
    encoded_jwt =jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    print('获取当前用户user :', user)
    print('获取当前用户type :', type(user))
    return user
# 获取当前激活用户
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user




# name = johndoe    password = secret
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1、验证用户
    user = authenticate_user(fake_users_db, form_data.username, form_data.password) # 验证用户
    # 2、access_token_expires访问令牌过期
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # timedelta表示两个datetime对象之间的差异。（来自datetime包）
    # 3、create_access_token创建访问令牌
    access_token = create_access_token(data={"sub": user.username}, 
                                expires_delta=access_token_expires)
    # 返回
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]






if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)