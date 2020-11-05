from fastapi import FastAPI,status
from pydantic import BaseModel
from typing import Optional,Set
from fastapi.encoders import jsonable_encoder

app =FastAPI()
class Item(BaseModel):
    name:str
    description:Optional[str] =None
    price:float
    tax:Optional[float] =None
    tags:Set[str] =[]

@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=['items'],summary="this is a summmary",
    description="this is a des",
    response_description="response_description",
    deprecated=True,
)
async def create_item(item:Item):
    '''
    tags,标签，用于'/doces/',参数后面跟list
    summary 摘要
    description 描述
    response_description 回应描述
    deprecated 表示已经弃用，但是不删除
    '''
    #jsonable_encoder 可把pydantic模型转换为dict类型，转换后的数据可以直接扔到json.dumps里
    json_compatible_data =jsonable_encoder(item) 
    fake_db[id] =json_compatible_data

    return item

@app.get("/items/",tags=["items"])
async def read_items():
    return [{"name":"foo","price":42}]

@app.get("/users/",tags=["users"])
async def read_users():
    return [{"username":"johndoe"}]

