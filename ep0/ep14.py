from typing import List 
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app =FastAPI()

class Item(BaseModel):
    name:str =None
    title:str =None
    proce:float =None
    tax:float =10.5
    tags :List[str] =[]

items ={
    "foo":{"name":"foo","price":50.2},
    "bar":{"name":"bar","title":"the baetenders","proce":62,"tax":20},
    "baz":{"name":"baz","price":50.2,"tax":10.5,"tags":[]}
}

@app.put("/items/{item_id}",response_model=Item)
async def update_item(item_id:str,item:Item):
    '''
        功能：用于数据的更新。
    '''
    update_item_encoded =jsonable_encoder(item)
    items[item_id] =update_item_encoded
    return update_item_encoded

@app.patch("/items/{item_id}",response_model=Item)
async def update_partitem(item_id:str,item:Item):
    '''
    部分更新，使用PATHC替换PUT
    检索存储数据
    将数据放入pydantic模型中
    dict从输入模型中生成没有默认值的 使用exclude_unset
        这样，就只能更新用户实际设置的值，而不是覆盖已经与默认值一起存储在模型的值
    创建存储模型的副本，使用接收到的部分更新，更新其属性
    将复制的模型转换为可以存储在数据库中的模型，使用jsonable_encoder
        类似于再次使用模型的.dict()方法，确保值之后可以转换成json的数据类型
    将数据存储到数据库
    返回更新模型
    '''
    stored_item_data =items[item_id]
    stored_item_model =Item(**stored_item_data)
    update_data =item.dict(exclude_unset=True)
    update_item =stored_item_model.copy(update=update_data)
    items[item_id] =jsonable_encoder(update_item)
    return update_item