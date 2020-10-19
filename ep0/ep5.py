from fastapi import FastAPI,Query,Path,Body
from typing import List,Optional,Set,Dict
from pydantic import Field,BaseModel
from pydantic import HttpUrl
import uvicorn

app =FastAPI()

class Image(BaseModel):
    '''
        HttpUrl的本质是字符串但是会被检测是不是为url的格式
    '''
    url:HttpUrl
    name:str

class Item(BaseModel):
    '''
        Image嵌套在这个表里
    '''
    name:str
    price:float
    tag_list:List[str] =[] #不会去重
    tag_set:Set[str] =set() #进行去重
    image:Image =None
    images:List[Image] =None

class offer(BaseModel):
    name:str
    items:List[Item]


@app.put("/items/{item_id}")
async def update_item(item_id:int,item:Item):
    results ={
        "item_id":item_id,
        "item":item
    }
    return results

@app.post("/offer/")
async def create_offer(offer:offer):
    return offer

@app.post("/images/")
async def create_images(Images:List[Image]):
    return Images

@app.post("/unknown_params/")
async def create_key(key_values:Dict[str,str]):
    '''
    对于未知的请求体参数，可以使用Dict键值对
    使用前from typing import Dict
    表示接收一个未知的的字符串类型的key以及字符串类型的值
    '''
    return key_values 


class example(BaseModel):
    name:str =Field(...,example='foo')
    price:float =Field(...,example='35.4')
    tax:float =Field(...,example="3.2")
    '''
    config会用做例子，所以key要对应，之后value的类型要对应
    Field声明中的example参数可以与config达到同样的目的
    也可以在视图函数中添加用body声明并这是example参数
    '''
    class Config:
        schema_extra={
            "example":{
                "name":"foo",
                "price":35.4,
                "tax":3.2
            }
        }
        
@app.put("/item/{item.id}")
async def update_config(item_id:int,item:example=Body(...,example={"name":"foo","price":35.4,"tax":3.2})):
    '''
        在pydantic里面创建实例类或者用Field声明pydantic模型或者在视图函数中用body声明，exmaple都可以达到同样的目的
    '''
    result ={
        "item_id":item_id,
        "item":item
    }
    return result

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)