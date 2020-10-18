#pip install fastapi
#pip install uvicorn

from typing import Optional
from fastapi import FastAPI
import uvicorn

from enum import Enum



'''
查询以及查询参数
'''
app =FastAPI()



class ModelName(str,Enum):
    '''
        定义枚举类型
        需要:
            from enum import Enum
            继承str,以及Eunm
    '''
    alexnet ="alexnet"
    resnet ="resnet"
    lenet ="lenet"



@app.get("/") #url地址
def read_root():
    return{"hello":"world"} #返回的响应体

@app.get("/items/{item_id}") 
def read_item(item_id:int,q:Optional[str] = None): 
    '''
    item_id为int类型，并且接收一个可选的参数为字符窜，默认值为none，若无none则这个参数是必须的
    '''
    return{"item_id":item_id,"q":q}

@app.get("/model/{model_name}")
async def read_moded(model_name:ModelName):
    '''
        匹配上面的枚举类型
    '''
    if model_name == ModelName.alexnet:
        return {
            "model_name":model_name,
            "message":"deep learning ftw"
        }
    if model_name ==ModelName.resnet:
        return {
            "model_name":model_name,
            "message":"have some residuals"
        }
    return{
            "model_name":model_name,
            "message":"lecnn all the images"
    }

@app.get('/files/{file_path:path}')
async def read_file(file_path:str):
    '''
    {file_path:path}
    :path 说明该参数应匹配任意路径
    若file_path参数开头为 /xxx/xx/x.text
    则url为/files//xxx/xx/x.text
    '''
    return{
        "filepath":file_path
    }

fake_items_db =[
    {"item_name":"Foo"},
    {"item_name":"Bar"},
    {"item_name":"Baz"},
]

@app.get("/itmesdefault/")
def read_itemsdict(skip:int = 0,limit:int =10):
    '''
    查询参数
    skip为int类型，默认值为0
    limit为int型，默认值为10
    当访问url为http://127.0.0.1:8000/itemsdict/ 等效访问 http://127.0.0.1:8000/itemsdict/?skip=0&limit=10
    当访问url为http://127.0.0.1:8000/itemsdict/?skip=20 等效访问 http://127.0.0.1:8000/itemsdict/?skip=20&limit=10
    未提供的参数值将使用默认值
    '''
    return fake_items_db[skip:skip+limit]

@app.get("/itemschoice/{name}")
def get_itemchoice(name:str,q:Optional[str] =None,short:bool =False):
    '''
        可选参数
        q为可选查询参数
        q的默认值为None
        short 的默认值为bool类型,False,也可以为0，no，false，off这些都等同于False，True等用于yes，1，true，on
        dict.update() 函数相当于往dict里添加键值对
        optional与可选参数没关系 与参数类型有关系
        optional是针对那些使用mypy的报错的情况使用的
    '''
    item ={"name":name}
    if q:
        item.update({"q":q})
    if short:
        item.update({"short":short})
    return item

@app.get("/users/{user_id}/items/{item_name}")
def get_useritems(user_id:int,item_name:str,q:Optional[str] =None,short:bool =False):
    '''
    可以同时声明多个参数
    user_id以及item_name
    '''
    item ={
        "userid":user_id,
        "itemname":item_name,
    }
    if q:
        item.update({"q":q})
    if short:
        item.update({"short":short})
    return item

@app.get("/user/{user_id}")
def get_userage(user_id:int,age:int):
    '''
    当参数没有默认值，则此参数为必须参数！
    Optional 必须后面给一个默认值，否则报错
    就像age，只给了数据类型，则为必须参数
    若访问时没有给age的值则报错
    '''
    return{
        "userid":user_id,
        "age":age,
    }

@app.get("/userinfo/{user_id}")
def get_userinfo(user_id:int,school_num:int,age:Optional[int] =None,email:str =None):
    '''
        接收多个参数
        schoole_num 为int类型必须参数
        age为int可选参数
        email为int可选参数
    '''
    userinfo ={
        "id":user_id,
        "school":school_num,
    }
    if email:
        userinfo.update({"email":email})
    if age:
        userinfo.update({"age":age})
    return userinfo



# if __name__ == "__main__":
#     uvicorn.run(app,host="127.0.0.1",port=8000)


#安装服务器
#pip install uvicorn
#命令运行服务器
#uvicorn main:app --reload
#交互式文档
#http://127.0.0.1:8000/docs
#可选api文档
#http://127.0.0.1:8000/redoc


#安装jinja2
#pip install jinja2
#安装静态文件
#pip install aiofiles
#安装
