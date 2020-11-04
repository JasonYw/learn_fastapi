from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app =FastAPI()

#浏览器把账号密码给服务器相关接口，验证后服务器把token给浏览器，浏览器需要携带token访问一些url
#tocken是有实效性

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='/token')
#声明该url是由客户端应用于获取令牌的url，该信息在openapi中使用，然后在交互式api文档系统中使用
#该oauth2_scheme 变量的一个实例OAuth2PasswordBearer 但它也是一个通知->告知后台


@app.get("/items")
async def read_items(token:str =Depends(oauth2_scheme)):
    return {"token":token}



