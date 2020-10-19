from fastapi import FastAPI,Query,Body,Path
from pydantic import BaseModel,Field
from typing import Set,List,Optional
from datetime import datetime,time,timedelta
from uuid import UUID
import uvicorn

app =FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id:UUID,
    start_datetime:Optional[datetime]=Body(None),
    end_datetime:Optional[datetime]=Body(None),
    repeat_at:Optional[time] =Body(None),
    proccess_after:Optional[timedelta] =Body(None),
):
    if start_datetime and end_datetime and repeat_at:
        start_process =start_datetime+proccess_after
        duration =end_datetime-start_datetime
        return{
            'item_id':item_id,
            'start_datetime':start_datetime,
            'end_datetime':end_datetime,
            'repeat_at':repeat_at,
            'proccess_after':proccess_after
        }
    return{
        "uuid":item_id
    }
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)