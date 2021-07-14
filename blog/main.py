from typing import final
from fastapi import FastAPI, Depends, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from . import schema, models
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=201)  
def create(request: schema.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

@app.get('/blog')
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.delete('/blog/{id}', status_code=204)
def delete(id: int, db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

@app.put('/blog/{id}', status_code= 202)
def update(id: int, request: schema.Blog,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= 404, detail=f'the post with id {id} not found')
    else:
        blog.update({'title': request.title, 'body': request.body},synchronize_session=False)
    db.commit()
    return 'Updated'

@app.get('/blog/{id}', status_code=200)
def show(id: int, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = 404, detail=f'blog with id {id} is not available')
    return blog




