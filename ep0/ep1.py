from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app =FastAPI()

'''
请求体
'''


class Item_model(BaseModel):
    '''
        创建数据模型
        其中有默认值的为可选参数，description与tax
    '''
    name:str
    description:Optional[str] =None
    price:float
    tax: Optional[float] =None

@app.post("/items/")
async def create_item(item:Item_model):
    return item
    
