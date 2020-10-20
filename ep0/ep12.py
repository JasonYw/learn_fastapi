from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse

app =FastAPI()
'''
错误处理 未完成
'''

items ={"foo":"the foo"}

@app.get("/items/{item_id}")
async def get_items(item_id:str):
    if item_id not in items:
        '''
        detail 除了传递str，还可以传递list、dict、这些都将转换成json数据
        在headers中定义错误信息
        '''
        raise HTTPException(
            status_code=404,
            detail="item not found",
            headers={"X-Error":"there goes my error"},
        )
    return {"item":items[item_id]}

#自定义异常处理器
class UnicornException(Exception):
    def __init__(self,name:str):
        self.name =name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request:Request,exc:UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message":f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.exception_handler(RequestVilidationError)
async def validation_exception_handler(request,exc):
    return PlainTextResponse(str(exc),status_code=400)

@app.get("/unicorns/{name}")
async def read_unicorn(name:str):
    if name =="yalo":
        raise UnicornException(name=name)
    return {"unicorn_name":name}


@app.get("/items/{item_id}")
async def read_item(item_id:int):
    if item_id ==3:
        raise HTTPException(status_code=418,detail="Nope")
    return {"item_id":item_id}


