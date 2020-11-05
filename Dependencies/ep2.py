from fastapi import FastAPI,Depends,Cookie


app =FastAPI()

def query_extractor(q:str =None):
    return q

def query_or_cookie_extractor(
    q:str =Depends(query_extractor),list_query:str =Cookie(None)
):
    if not q:
        return list_query
    return q


@app.get("/items")
async def read_query(query_or_default:str =Depends(query_or_cookie_extractor)):
    return {"q_or_cookie":query_or_default}


if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)