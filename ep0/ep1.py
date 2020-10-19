from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import uvicorn

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
    

class item_pjmodel(BaseModel):
    name:str
    price:float

@app.post('/items/{item_id}')
async def create_pj(item_id:int,item:item_pjmodel):
    '''
    item_pjmodel是pydantic模型的函数参数所以会从请求体中获取
    item_id会从url请求路径中获取
    '''
    return{
        "item_id":item_id,
        "postdata":item
    }


class item_pjpmodel(BaseModel):
    name:str
    price:int =None

@app.post('/item_pjp/{item_id}')
async def create_pjp(item_id:int,item:item_pjpmodel,page:int,age:int =None):
    '''
        函数参数查询顺序
            如果url中声明了该参数，则会被用作路径参数
            若参数属于单一类型，则被解释为查询参数
            若参数被声明为一个pydantic模型，将被解释为请求体
        page,age 为参数，其中page为必须参数，age为可选参数
        item 会从formdata里提取 因为item_pjpmodel为pydantic模型
        item_id会从url中提取
    '''
    item_dict =item.dict()
    item_dict.update({'page':page*item_id})
    if age:
        item_dict.update({'age':age})
    return item_dict

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)