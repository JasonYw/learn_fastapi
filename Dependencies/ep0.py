from fastapi import FastAPI,Depends
from pydantic import BaseModel

app =FastAPI()

async def common_parameters(q:str =None,skip:int=0,limit:int=100):
    #被依赖项
    limit += 66
    return {"q":q,"skip":skip,"limit":limit}

@app.get("/items/")
async def read_items(commons:dict =Depends(common_parameters)):
    #commons:dict = Depends(common_parameters) 相当于  commons:dict ={"q":q,"skip":skip,"limit":limit}
    #被依赖项必须是可调用的
    #Depends依赖注入
    #前提是有共享的逻辑
    #有共享的数据库连接
    #强制执行安全，身份验证，角色要求等
    commons['skip'] += 10
    return commons

@app.get("/users/")
async def read_users(commons:dict =Depends(common_parameters)):
    return commons