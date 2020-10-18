from fastapi import FastAPI,Cookie,Header
from typing import Optional,List

app =FastAPI()


@app.get("/items/")
async def read_items(ads_id:Optional[str]=Cookie(None)):
    '''
        from fastapi import Cookie
        要声明cookie需要使用Cookie
        否则会被解释为查询参数
    '''
    return {"ads_id":ads_id}

@app.get("/header/")
async def read_header(user_angent:Optional[str] =Header(None,convert_underscores=False)):
    '''
    Header() 额外功能，会提供一个转换功能把"-"转换成"_"
    所以添加convert_underscores=False禁用掉此功能
    但是某些Http代理或者服务器不允许使用带下划线的标头
    '''
    return {"User-Agent":user_angent}

@app.get("/header_list")
async def read_headerlist(x_tocken:List[str] =Header(None)):
    '''
    若headers中有多个值时，定义成List即可，响应头内容本质为str，所以是List[str]
    '''
    return {"x_tocken":x_tocken}

