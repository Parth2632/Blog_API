from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine , session_local
import models 
import schemas

models.Base.metadata.create_all(bind=engine) #create a table

app = FastAPI()
#DB dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return{
        "Message": "Welcome to Blog API"
    }

#Create Blog
@app.post("/blogs" , response_model=schemas.BlogResponse)
def create_blog(blog : schemas.BlogCreate , db : Session = Depends(get_db)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog 

#Read blogs
@app.get("/blogs",response_model=list[schemas.BlogResponse])
def read_blogs(db : Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    if all_blogs is None:
        raise HTTPException(status_code=404,detail="No blogs found")
    return all_blogs


#Read a single blog
@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
def read_blog(id : int , db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=404,detail="Blog not found")
    return blog

#update blog
@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update_blog(id : int , blog : schemas.BlogCreate,db : Session = Depends(get_db)):
    update = db.query(models.Blog).filter(models.Blog.id == id).first()
    if update is None:
        raise HTTPException(status_code=404,detail="Blog not found")
    update.title = blog.title
    update.content = blog.content
    db.commit()
    db.refresh(update)
    return update

#delete blog api
@app.delete("/blogs/{id}")
def delete_blog(id : int , db : Session = Depends(get_db)):
    delete = db.query(models.Blog).filter(models.Blog.id == id).first()
    if delete is None:
        raise HTTPException(status_code=404,detail="Blog not found")
    db.delete(delete)
    db.commit()
    return {"message" : "Blog deleted successfully"}   

