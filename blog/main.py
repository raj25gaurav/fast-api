from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Step 1: Define a schema
class Blog(BaseModel):
    title: str
    body: str

class BlogOut(Blog):
    id: int

# In-memory "database"
blogs = []
blog_id_counter = 1

# Step 2: Create a blog
@app.post("/blog", response_model=BlogOut)
def create_blog(blog: Blog):
    global blog_id_counter
    new_blog = {
        "id": blog_id_counter,
        "title": blog.title,
        "body": blog.body
    }
    blogs.append(new_blog)
    blog_id_counter += 1
    return new_blog

# Step 3: Get all blogs or filter by title
@app.get("/blogs", response_model=List[BlogOut])
def get_blogs(title: Optional[str] = None):
    if title:
        filtered = [blog for blog in blogs if title.lower() in blog["title"].lower()]
        return filtered
    return blogs

# Step 4: Get a single blog by ID
@app.get("/blog/{blog_id}", response_model=BlogOut)
def get_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

# Step 5: Delete a blog by ID
@app.delete("/blog/{blog_id}")
def delete_blog(blog_id: int):
    for index, blog in enumerate(blogs):
        if blog["id"] == blog_id:
            deleted = blogs.pop(index)
            return {"message": "Blog deleted", "blog": deleted}
    raise HTTPException(status_code=404, detail="Blog not found")