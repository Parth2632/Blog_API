"""FastAPI Blog API

Provides CRUD operations for blog posts with JWT authentication.
"""
from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import engine, session_local
import models
import schemas
from auth import verify_token, create_token, verify_credentials  # add verify_credentials

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", version="1.0.0")


# ── DB dependency ────────────────────────────────────────────────────────────

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# ── Home ─────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Welcome to Blog API"}


# ── Auth ─────────────────────────────────────────────────────────────────────

@app.post("/login")
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Accept real credentials instead of issuing a token to anyone.
    verify_credentials should look up the user and check the password hash.
    """
    user = verify_credentials(credentials.username, credentials.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_token({"sub": str(user.id), "username": user.username})


# ── Blogs ────────────────────────────────────────────────────────────────────

@app.post("/blogs", response_model=schemas.BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_token),
):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        owner_id=user["sub"],          # tie the blog to its author
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blogs", response_model=schemas.BlogListResponse)
def read_blogs(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, ge=1, le=100),
    search: str = Query(default=None),
):
    """
    Two bugs fixed:
      1. Filter BEFORE offset/limit so pagination counts are correct.
      2. .all() returns [] not None, so the old `is None` guard never fired.
    """
    query = db.query(models.Blog)

    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    blogs = query.offset((page - 1) * limit).limit(limit).all()

    return {"total": total, "page": page, "limit": limit, "blogs": blogs}


@app.get("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


@app.put("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(
    blog_id: int,
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_token),
):
    existing = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    # Prevent users from editing each other's posts
    if str(existing.owner_id) != user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your blog")

    existing.title = blog.title
    existing.content = blog.content
    db.commit()
    db.refresh(existing)
    return existing


@app.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_token),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    if str(blog.owner_id) != user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your blog")

    db.delete(blog)
    db.commit()