from fastapi import Depends,FastAPI,Header,HTTPException


app =FastAPI()

async def verify_tocken(x_tocken:str =Header(...)):
    if x_tocken != "fake-super-secret-token":
        raise HTTPException(status_code=400,detail="x-token header invalid")

async def verify_key(x_key:str =Header(...)):
    print(x_key)
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400,detail="x-key header invalid")


@app.get("/items/",dependencies =[Depends(verify_key),Depends(verify_tocken)])
async def read_items():
    return [{"item":"foo"},{"item":"bar"}]

