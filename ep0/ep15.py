from fastapi import FastAPI,Depends,Header,Cookie,HTTPException
from dbsession import DBSession
app =FastAPI()
'''
依赖关系
'''

async def common_parameters(q:str=None,skip:int=0,limit:int=10):
    '''
    创建依赖
    函数
    '''
    return {"q":q,"skip":skip,"limit":limit}


class CommonQueryParams:
    '''
    创建依赖
    类
    ''' 
    def __init__(self,q:str=None,skip:int=0,limit:int=100):
        self.q =q
        self.skip =skip
        self.limit =limit

@app.get("/items/",summary="learn functions depends",tags=["1"])
async def read_items(commons:dict=Depends(common_parameters)):
    '''
    声明依赖
    注：Depends只接受一个函数类型的参数或一个类名
    工作流程：请求->调用依赖->拿到依赖的函数的返回结果->把返回结果传递给路径操作函数中对应参数
    '''
    return commons

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/users/",summary="learn class depends",tags=["2"])
async def read_users(commons:CommonQueryParams =Depends(CommonQueryParams)):
    respones={}
    if commons.q:
        respones.update({"q":commons.q})
    items =fake_items_db[commons.skip:commons.skip+commons.limit]
    respones.update({"items":items})
    return commons

'''
子依赖
'''
def query_extractor(q11:str=None,q12:str=None):
    #声明第一个依赖函数
    '''
    若某个依赖项在同一个路径操作中被声明了多次，例如多个依赖项都有一个共同的子依赖项，
    那么fastapi默认在每一次请求中只会调用依赖性一次。
    因为fastapi会把这个依赖项返回值缓存起来，然后把这个值传递给所需要到依赖项
    而不是在同一次请求中多次调用这个依赖项。
    如需要多次调用，不要缓存值，则需要使用参数use_cache=False来禁止依赖项的缓存
    '''
    try:
        return q11 + q12
    except:
        return None

def query_or_cookie_extractor(q2:str =Depends(query_extractor),last_query:str=Cookie("aaa")):
    #声明第二个依赖函数
    if q2:
        return q2
    return last_query

@app.get("/items_child/",summary="learn_child_depends",tags=['3'])
async def read_query(query_or_default:str =Depends(query_or_cookie_extractor)):
    '''
    请求->子依赖->获取子依赖返回值->依赖->获取依赖返回值->把返回结果传递给路径操作函数中对应参数
    '''
    return {"q_or_cookie":query_or_default}


'''
不需要依赖项的返回值，但是仍然需要依赖项被执行。在这种情况下，我们可以通过路径操作装饰器，来操作依赖项的的一个列表
'''
async def verify_token(x_token:str=Header(...)):
    if x_token !="token":
        raise HTTPException(status_code=400,detail="X-Token header invalid")

async def verify_key(x_key:str=Header(...)):
    if x_key != "key":
        raise HTTPException(status_code=400,detail="x-key header invalid")
    return x_key

@app.get("/decorator/",dependencies=[Depends(verify_token),Depends(verify_key)],summary="decorator depends",tags=['4'])
async def read_decorator():
    '''
    此依赖项与普通依赖项的执行相同，但他们的返回值不会被传递给路径操作函数
    我们可以重复使用已经声明的依赖项，无论他们是否有返回值，都不会影响依赖项的执行
    '''
    return [{"item":"foo"},{"item":"bar"}]

'''
yield功能的依赖性
yield代替return
'''
async def get_db():
    db =DBSession()
    try:
        '''
        不要尝试在yield后面抛出HTTPException，不会起作用
        yield之后的退出，是在异常处理器之后被执行的
        '''
        yield db
    finally:
        db.close()

async def dependency_a():
    dep_a =generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()

async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b =generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)

async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c =generate_dep_c()
    try:
        yield  dep_c
    finally:
        dep_c.close(dep_b)

class MySuperContextManager:
    def __init__(self):
        self.db =DBSession()

    def __enter__(self):
        return self.db
    
    def __exit__(self,exc_type,exc_value,traceback):
        self.db.close()
    
async def get_db():
    with MySuperContextManager() as db:
        yield db
        