from typing import List,Optional
from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
import uvicorn

app =FastAPI()


 
class Item(BaseModel):
    name:str
    price:float
    tax:float =None
    tags:List[str] =[]

@app.post("/items/",response_model=Item)
async def create_item(item:Item):
    '''
    Response模型可以是一个pydantic模型，也可以是一个Pydantic模型的列表,List[Item]
    FastAPI利用Response模型实现以下功能
        将输出数据转换成声明的response模型
        对数据进行校验
        生成自动化文档
        最总要的是限制输出数据只能是声明的response模型
    '''
    return item


class Userin(BaseModel):
    '''
    需要pip install pydantic[email]
    '''
    username:str
    password:str
    email:EmailStr
    full_name:str =None

class Userout(BaseModel):
    username:str
    email:EmailStr
    full_name:str =None

@app.post("/user/",response_model=Userout)
def create_user(*,user:Userin):
    '''
        虽然返回的user是Userin模型包含了password关键字
        但是我们声明的response模型Userout不包含password
        FastAPI会过滤掉所有不在输出模型中的数据，因此结果里没有password
    '''
    return user


class fruit(BaseModel):
    name:str
    price:float
    tax:float =None

items={
    "apple":{"name":"apple","price":50},
    "orange":{"name":"orange","price":30},
    "bannana":{"name":"bannana","price":20,"tax":10},
}

@app.get("/fruit/{item_id}",response_model=fruit,response_model_exclude_unset=True)
def get_fruitprice(item_id:str):
    '''
    response_model_exclude_unset=True
    此参数的作用是，因为模型里可以有可选参数，若可选参数没有被赋值，则直接忽略掉
    但是默认值的类型与字段要求类型相同时，则不会被排除
    response_model_exclude_defaults=True
    response_model_exclude_none=True
    上述两个参数也可以达到同样的效果
    '''
    return items.get(item_id)


@app.get("/fruit_include/{item_id}",response_model=fruit,response_model_include={"name"})
def get_fruitprice(item_id:str):
    '''
    返回的内容只包含name字段的值
    '''
    return items.get(item_id)

@app.get("/fruit_exclude/{item_id}",response_model=fruit,response_model_exclude={"name"})
def get_fruitprice(item_id:str):
    '''
    返回的内容除了name字段的值 其余全部返回
    '''
    return items.get(item_id)
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)