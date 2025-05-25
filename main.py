from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Blog(BaseModel):
    title:str 
    body:str 
    published:Optional[bool]

@app.post('/blog')
def create_blog(blog:Blog):
    return {'data': f"Blog is created with title as {blog.title}"}

@app.get('/blog')
def index(limit,published):
    if published:
        return {'data': f'{limit} blogs  from the db'}
    else:
        return {'data': f'{limit} blogs from db'}
@app.get('/blog/{id}/comments')
def comments(id):
    return {'data': ['1', '2']}

@app.get('/')
def index():
    return {'data': {'name':'Sarthak'}}

@app.get('/about')
def about():
    return{'data': 'about page'}
