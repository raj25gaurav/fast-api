from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Step 1: Define a schema
class Blog(BaseModel):
    title: str
    body: str

# Step 2: Use the schema in your route
@app.post('/blog')
def create(blog: Blog):
    return {
        'title': blog.title,
        'body': blog.body
    }