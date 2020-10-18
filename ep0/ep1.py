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
        optional不要轻易加
    '''
    name:str
    description:str = None
    price:float
    tax: float = None

@app.post("/items/")
async def create_item(item:Item_model):
    '''
    return的是item不是Item_model
    结果
        将请求体作为json读取
        转换为相应的数据类型
        校验数据
            数据无效会返回错误信息
        接收的数据会放在item中
        可将接收的item对象转换成字典类型
    '''
    item_dict =item.dict()
    if item.tax:
        price_with_tax =item.price+item.tax
        item_dict.update({
            "price_with_tax":price_with_tax
        })
    return item_dict
    
