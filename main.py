from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.get('/')
def index(limit: int , published: bool):
    if(published):
        return {'returned all the blogs'}
    else:
        return {'data': f'blog list of limit {limit}'}

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}

@app.post('/blog')
def blog(blog: Blog):
    return blog