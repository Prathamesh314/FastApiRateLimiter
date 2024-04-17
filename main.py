from typing import Optional

from fastapi import FastAPI
from redismanager import *



app = FastAPI()
TOKEN_BUCKET = None
TOKEN_BUCKET = get_token_bucket("test", 11) if TOKEN_BUCKET is None else TOKEN_BUCKET
print(f"{TOKEN_BUCKET=}")
@app.get("/")
def read_root():
    global TOKEN_BUCKET
    print(f"{TOKEN_BUCKET.size()=}")
    if TOKEN_BUCKET.size() > 1:
        print("1 token is consumed.")
        TOKEN_BUCKET.consume()
        return {"Hello": "World"}
    elif TOKEN_BUCKET.exists():
        return {"response": "Too many api requests"}
    else:
        TOKEN_BUCKET = get_token_bucket("test", 11)
        # return {"response": "created new token bucket"}
        TOKEN_BUCKET.consume()
        return {"Hello":"World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}