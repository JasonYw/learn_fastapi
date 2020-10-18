#pip install fastapi
#pip install uvicorn

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app =FastAPI()


class Item(BaseModel):
    name:str
    price:float 
    is_offer :Optional[bool] =None

@app.get("/") #url地址
def read_root():
    return{"hello":"world"} #返回的响应体

@app.get("/items/{item_id}") 
def read_item(item_id:int,q:Optional[str] = None): #item_id为int类型，并且接收一个可选的参数为字符窜，默认值为none，若无none则这个参数是必须的
    return{"item_id":item_id,"q":q}

@app.put("/items/{item_id}")
def update_item(item_id:int,item:Item):
    return {"item_name":item.name,"item_id":item_id}


#命令运行服务器
#uvicorn main:app --reload
#交互式文档
#http://127.0.0.1:8000/docs
#可选api文档
#http://127.0.0.1:8000/redoc