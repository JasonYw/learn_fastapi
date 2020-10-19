from fastapi import FastAPI,status,Response,Body
from fastapi.responses import JSONResponse

app =FastAPI()

@app.post("/items/",status_code=201)
async def create_item(name:str):
    '''
    status_code为http状态码，属于装饰器的参数
    '''
    return {"name":name}

tasks ={
    "foo":{"name":"listen to the aa"},
    "bar":{"name":"hhhhh"}
}



@app.get("/foo/{task_id}",status_code=200)
def get_foo(tasks_id:str,response:Response):
    '''
    可以在路径函数参数中声明一个response，类型为Response
    Response -> from fastapi import Response
    Response里封装了常用的状态码
    '''
    if tasks_id not in tasks:
        tasks[tasks_id] ="this didn't exists before"
        response.status_code =status.HTTP_201_CREATED
    return tasks[tasks_id]


@app.get("/statuecode/{item_id}")
async def unpsert_item(item_id:str):
    '''
    可以通过response对象来设置状态码，
    from fastapi.responses import JSONResponse
    但是要导入JSONResponse
    
    '''
    if item_id in tasks:
        return tasks[item_id]
    else:
        return JSONResponse(status_code=status.HTTP_201_CREATED,content=tasks)
