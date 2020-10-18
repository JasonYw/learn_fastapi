from fastapi import FastAPI
from typing import Optional
from typing import List
from pydantic import BaseModel
from fastapi import Path
from fastapi import Query
from fastapi import Body
app =FastAPI()

'''
    路径参数和数值校验
'''


@app.get("/item/{item_id}")
async def get_items(item_id:int =Path(...,title='ID of the item'),q:str =Query(None,alias="item-query")):
    '''
    校验路径参数
    首先from fastapi import Path
    第一个参数...则声明此参数是必须的,又因为路径参数总是必须的所以必须为...
    '''
    result ={
        'itemid':item_id,
    }
    if q:
        result.update({'q':q})
    return result

@app.get("/itmes_sort/{item_id}")
async def get_itemssort(q:str,item_id:int =Path(...,title='hello')):
    '''
    参数排序，
    一个必须参数q而且无需使用Query()声明
    一个需要Path声明的路径参数item_id
    则q必须放在item_id之前，否则python报错
    若不想按照上面的规则，可以写成  -> def get_itemssort(*,item_id:int =Path(...,title='hello'),q:str):
    把第一参数写成*，则其他参数被称为kwargs
    '''
    return '200'

@app.get("items_int/{item_a}")
async def get_itemsint(*,item_a:int =Path(...,ge=10,le=100),q:str):
    '''
    ge =1 代表item_a必须大于等于1
    le =1 代表item_a必须小于等于1
    gt  表示大于
    lt  表示小于
    '''
    item ={
        'item_a':item_a,
        'q':q,
    }
    return item


class user_id(BaseModel):
    id:int
    name:str
    card:str =None

class user_profile(BaseModel):
    id:int 
    age:int =None
    email:str =None

@app.put("/item_put/{item_id}")
async def get_itemput(*,item_id:int =Path(...,gt=1,lt=500),q:int=None,user_base:user_id,user_extra:Optional[user_profile]=None,importance:int =Body(...)):
    '''
        发送请求时一定要注意','
        注意：
            put的时候,user_extra是可选参数，如果有，则必须有id，age与email变成可选的
            user_base是必选参数，但是其中card是可选参数，id与name是必选参数
        Body
            from fastapi import Body
            若请求体出现单一值，FastAPI 会误将其认为是参数处理，所以需要Body声明他是请求体中的
            例importance 为请求体必选参数，但不是url中的
            Body具有Query与Path以及其他后面看到的类完全相同的额外校验和元数据参数
    '''
    item={
        'id':item_id,
        "item_base":user_base,
        'importance':importance
    }
    if q:
        item.update({"q":q})
    if user_extra:
        item.update({"user_extra":user_extra})
        '''
        请求体：
        {
            "user_base": {必选
                "id": 0,  选了必选
                "name": "string", 选了必选
                "card": "string" 选了依然可选
            },
            "user_extra": { 可选
                "id": 0, 选了就必选
                "age": 0, 选了依然可选
                "email": "string" 选了依然可选
            },
            "importance": 1 必选
        }
        响应体：
            {
                "id": 2,
                "item_base": {
                    "id": 0,
                    "name": "string",
                    "card": "string"
                },
                "importance": 1,
                "user_extra": {
                    "id": 0,
                    "age": 0,
                    "email": "string"
                }
            }
        '''
    
    return item


class singal(BaseModel):
    id:int
    name:str
    age:int =None

@app.put("/item_bodysignal/{item_id}")
def put_bodysingnal(*,item_id:int =Path(...,lt=100,gt=1),item_sg:singal =Body(...,embed=True)):
    '''
        使用Body声明之后，并且参数embed=True，就将singal嵌套了一个{}中
        请求体
            {
                "item_sg": {
                    "id": 0,
                    "name": "string"
                    'null':null
                }
            }
        响应体
            {
                "item_id": 2,
                "profile": {
                    "id": 0,
                    "name": "string",
                    "age": null
                }
            }
    '''
    result ={
        'item_id':item_id,
        'profile':item_sg
    }
    return result
