from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

app = FastAPI(
    title="Blog API",
    description="A simple blog API with CRUD operations",
    version="1.0.0"
)

# In-memory data store
fake_blog_db = {}

# Pydantic models
class Blog(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    body: str = Field(..., min_length=10)

class BlogCreate(Blog):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    body: Optional[str] = Field(None, min_length=10)

class BlogResponse(Blog):
    id: str

# Pre-populate with dummy blogs
for i in range(1, 4):
    blog_id = str(uuid4())
    fake_blog_db[blog_id] = {
        "title": f"Sample Blog {i}",
        "body": f"This is the content of sample blog {i}."
    }

# Routes
@app.post('/blog', response_model=BlogResponse, status_code=201, tags=["Blogs"])
def create_blog(blog: BlogCreate):
    blog_id = str(uuid4())
    fake_blog_db[blog_id] = blog.dict()
    return {**blog.dict(), "id": blog_id}

@app.get('/blogs', response_model=List[BlogResponse], tags=["Blogs"])
def get_all_blogs(limit: int = Query(10, le=100), skip: int = 0):
    blogs = [
        {"id": blog_id, **data}
        for blog_id, data in list(fake_blog_db.items())[skip: skip + limit]
    ]
    return blogs

@app.get('/blog/{blog_id}', response_model=BlogResponse, tags=["Blogs"])
def get_blog(blog_id: str = Path(..., description="The ID of the blog to retrieve")):
    if blog_id not in fake_blog_db:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {**fake_blog_db[blog_id], "id": blog_id}

@app.put('/blog/{blog_id}', response_model=BlogResponse, tags=["Blogs"])
def update_blog(blog_id: str, blog: BlogUpdate):
    if blog_id not in fake_blog_db:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    stored_blog_data = fake_blog_db[blog_id]
    updated_data = blog.dict(exclude_unset=True)
    stored_blog_data.update(updated_data)
    fake_blog_db[blog_id] = stored_blog_data
    return {**stored_blog_data, "id": blog_id}

@app.delete('/blog/{blog_id}', status_code=204, tags=["Blogs"])
def delete_blog(blog_id: str):
    if blog_id not in fake_blog_db:
        raise HTTPException(status_code=404, detail="Blog not found")
    del fake_blog_db[blog_id]
    return

@app.get('/search', response_model=List[BlogResponse], tags=["Blogs"])
def search_blogs(keyword: str = Query(..., min_length=3, description="Keyword to search in blog titles")):
    result = []
    for blog_id, blog in fake_blog_db.items():
        if keyword.lower() in blog['title'].lower():
            result.append({**blog, "id": blog_id})
    return result

# Health check
@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "OK", "version": app.version}