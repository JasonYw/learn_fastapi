from fastapi import FastAPI,Path
from pydantic import BaseModel,EmailStr
from typing import Optional,Union,List,Dict

app =FastAPI()

class UserBase(BaseModel):
    username:str
    email:EmailStr 
    full_name:str=None

class Userin(UserBase):
    password:str
    
class Userout(UserBase):
    pass

class Userindb(UserBase):
    hashed_password:str

def fake_pass_user(raw_password:str):
    return "supersecret"+raw_password

def fake_save_user(userin:Userin):
    ditc_ =userin.dict()
    user_in_db =Userindb(**userin.dict(),hashed_password=fake_pass_user(userin.password))
    print("user saved")
    return user_in_db

@app.post("/user/",response_model=Userout)
def create_user(userin:Userin):
    user_saved =fake_save_user(Userin)
    return user_saved

class goodsbase(BaseModel):
    title:str
    type:str

class caritem(goodsbase):
    type ="car"

class planeitem(goodsbase):
    type ="plane"
    size:int

item1 ={
    1:{
        "title":"drive car",
        "type":"car"
    },
    2:{
        "title":"airplane",
        "type":"plane",
        "size":5,
    }
}

item2 =[
    {"type":"bike","title":"drive bike"},
    {"type":"train","title":"drive train"}
]

@app.get("/goods/{item_id}",response_model=Union[caritem,planeitem])
async def get_goods(item_id:int =Path(...,lt=3,gt=0)):
    return item1[item_id]

@app.get("/goods1/{item_id}",response_model=List[goodsbase])
async def get_goood1(item_id:int =Path(...,lt=2,ge=0)):
    '''
    无法返回item2[0] 或者 item[1]
    因为response_model 要求首先是一个List，之后每一个元素是一个pydantic模型
    '''
    return item2

@app.get("/goods2/{item_id}",response_model=goodsbase)
async def get_goood1(item_id:int =Path(...,lt=2,ge=0)):
    '''
    因为返回模型为一个pydantic模型，又因为item2中的元素都符合goodsbase，
    所以可以返回其中的元素
    '''
    return item2[item_id]

@app.get("/goods3/",response_model=Dict[str,float])
async def get_goods3():
    '''
    当不确定具体值以及key的名称，
    可以直接把返回类型规定为Dict，from typing import Dict
    但是需要规定key的类型以及value的类型
    上述规定了key为字符型，value为浮点数
    '''
    return {"aaaa":1.1}