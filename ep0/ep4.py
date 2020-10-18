from fastapi import FastAPI,Query,Body,Path
from pydantic import BaseModel
from pydantic import Field
from typing import Optional

app =FastAPI()

class Item(BaseModel):
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





