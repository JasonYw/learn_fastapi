from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Query
from typing import List
from typing import Optional
import uvicorn

app =FastAPI()

'''
    字符串校验
'''


@app.get("/items/")
async def get_items(q:str = Query(None,max_length=50,min_length=3,regex="^re")):
    '''
    from fastapi import Query
    Query()用来做校验工作
    第一个参数None为默认值，标记为可选参数，
    ！！！若第一个参数为... 也就是Query(...) 则声明此函数为必须参数
    第二个为最大长度，也就是q参数长度不能超过50
    第三个为最小长度，也就是q参数长度要大于3
    regex则为正则表达式，限制了此参数必须以re开头
    Query(None) 会显式的将其声明为查询参数

    '''
    if q:
        return {"q":q}
    else:
        return '200'


@app.get("/items_list/")
async def get_itemslist(q:Optional[List[str]] =Query(None)):
    '''
        若url中存在多个参数q，
        首先使用from typing import Optional，List
        则使用Optional[List[str]]来声明
        也可以q:List[str]
        若要声明q为List必须使用Query 否则q将被解释为请求体
    '''
    query_items ={"q":q}
    return query_items


@app.get("/itemdefault_list/")
async def get_itemdefault(q:List[str] =Query(['bar','foo'])):
    '''
        可以用Query给q list类型赋予默认值
        若q:list = Query([]),则这种情况下fastapi不会检查列表的内容
        List[int]将检查list中必须为整数，但是list不会
    '''
    query_item ={'q':q}
    return query_item


@app.get("/items_fortools/")
async def get_itemsdefault(q:Optional[str] =Query(None,title='for tools',description='for tools',min_length=3,deprecated=True)):
    '''
        title以及description是提供给外部文档使用的
        deprecated=True 表示此参数已经被弃用，会在http://127.0.0.1:8000/docs文档中标记出来，但是程序中依然有效
    '''
    return '200'

@app.get("/items_alias/")
async def get_itemsalias(q:Optional[str] =Query(None,alias="item-query")):
    '''
        url地址将为http://127.0.0.1:8000/items_alias/?item-query="hello"
        则q的值为hello，alias参数就是给q起一个别名，url可以使用该别名
    '''
    if q:
        return {'q':q}
    return '200'

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)