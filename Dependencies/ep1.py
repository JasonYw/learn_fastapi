from fastapi import FastAPI,Depends


app =FastAPI()

fake_items_do =[
    {"items_name":"foo"},
    {"items_name":"bar"},
    {"items_name":"baz"}
]

class CommonqueryParams():
    def __init__(self,q:str=None,skip:int=0,limit:int=100):
        self.q =q
        self.skip =skip
        self.limit =limit
    


@app.get("/items/")
async def read_items(commans:CommonqueryParams =Depends(CommonqueryParams)):
    #commans:CommonqueryParams =Depends(CommonqueryParams) 与commans =Depends(CommonqueryParams) 效果一样
    #commans:CommonqueryParams =Depends() 也可以 但是有条件 被依赖项必须是一个类，并且相关性是明确的
    response ={}
    if commans.q:
        response.update({"q":commans.q})
    items =fake_items_do[commans.skip:commans.skip+commans.limit]
    response.update({"items":items})
    return response