from fastapi import FastAPI,Form,File,UploadFile
from typing import List
from fastapi.responses import HTMLResponse
'''
要想使用表格首先pip install python-multipart
要接收上传的文件首先pip install python-multipart
'''
app =FastAPI()

@app.post("/login/")
async def login(username:str =Form(...),password:str =Form(...)):
    '''
        Form 与 Body参数类似区别是 一个前者是formdata 一个是json
        Form继承的Body
        FORM ->requests.post(url,data=data)
        BODY ->requests.post(url,json=data)
    '''
    return {"username":username}

@app.post("/files/")
async def create_file(file:bytes=File(...)):
    '''
    声明文件主体，需要使用File，否则参数会被解释称查询参数或者json参数
    若file的期待类型为bytes，fastapi将读取文件
    这些会临时存在内存中
    '''
    return {"file_size":len(file)}

@app.post("/uploadfiles/")
async def create_upload_file(file:UploadFile =File(...)):
    '''
    若期望的类型为UploadFile，则比bytes会有一些有点
    当文件超过内存大小时，文件将存在磁盘中
    所以适合大型文件
    可以从上传的文件中获得元数据
    UploadFile 具有以下属性：
        filename 原始文件的名字
        content_type 文件类型 例如 image/jpeg
        file 一个TemporaryFile
    UploadFile 具有以下方法：
        write(data) 将data bytes或者str 写入文件    
        read(size) 读取(int)个文件的字节/字符
        seek(offset) 转到文件中（offset：int）字节位置
            例如 file.seek(0) 转到字节开头
            例如 await file.read() 读一次 回来再次读取 这个功能将很有用
        close() 关闭文件
    上述方法都是async方法，都需要加await
        例如 contents =await file.read()

    '''
    return {"filename":file.filename}

@app.post("/fileslist/")
async def create_filelist(files:List[bytes] =File(...)):
    return {"file_size":[len(file) for file in files]}

@app.post("/uploadfileslist/")
async def create_upload_filelist(files:List[UploadFile] =File(...)):
    return {"filenames" : [file.name for file in files]}

@app.get("/")
async def main():
    content ="""
        <body>
            <form action="/files/" enctype="multipart/form-data" method="post">
                <input name="file" type="file" multiple>
                <input type="submit">
            </form>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
                <input name="file" type="file" multiple>
                <input type="submit">
            </form>
        </body>
        """
    return HTMLResponse(content=content)
    


@app.post("/file_1/")
async def create_file_1(file:bytes =File(...),fileb:UploadFile =File(...),token:str =Form(...)):
    return{
        "file_size":len(file),
        "token":token,
        "fileb_cotent_type":fileb.content_type
    }

