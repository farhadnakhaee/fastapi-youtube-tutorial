from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


# path parameter
@app.get("/blog/{id}")
def index(id: int):
    return {'data': {'id': id, 'name': 'Farhad', 'Email': 'nakhaee.farhad@gmail.com'}}


# query parameter
@app.get("/blog/")
def index(limit = 10, published: bool = True, sort: Optional[str] = ""):
    if published:
        return {'data': f'{limit}{sort} published blogs from the db'}
    else:
        return {'data': 'no published blogs from the db'}

# post opration
# request body


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
     return {'data': f"Blog is created with title as -{blog.title}-"}