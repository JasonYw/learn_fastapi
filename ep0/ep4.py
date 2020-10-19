from fastapi import FastAPI,Query,Body,Path
from pydantic import BaseModel
from pydantic import Field
from typing import Optional
import uvicorn

app =FastAPI()

class Item(BaseModel):
    '''
        from pydantic import Field
        Filed将声明pydantic模型内部的生命校验和元数据
    '''
    name:str
    title:str=Field(
        None,title='the title of the item',max_length=50
    )
    price:float=Field(...,gt=0)


@app.put("/items/{item_id}")
async def put_items(item_id:int,item_profile:Item=Body(...,embed=True)):
    result ={
        'item_id':item_id,
        "item":item_profile,
    }
    return result

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)



