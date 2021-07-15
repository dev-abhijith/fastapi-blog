from typing import final, List
from fastapi import FastAPI, Depends, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from . import schema, models
from .database import SessionLocal, engine
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post('/blog', status_code=201, tags=['Blog'])  
def create(request: schema.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schema.ShowBlog], tags=['Blog'])
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.delete('/blog/{id}', status_code=204, tags=['Blog'])
def delete(id: int, db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted'


@app.put('/blog/{id}', status_code= 202, tags=['Blog'])
def update(id: int, request: schema.Blog,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= 404, detail=f'the post with id {id} not found')
    else:
        blog.update({'title': request.title, 'body': request.body},synchronize_session=False)
    db.commit()
    return 'Updated'


@app.get('/blog/{id}', status_code=200, response_model=schema.ShowBlog, tags=['Blog'])
def show(id: int, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = 404, detail=f'blog with id {id} is not available')
    return blog

# Users ---------------------------------------------------------------



@app.post('/user', status_code=201, tags=['User'])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', response_model=List[schema.ShowUser], tags=['User'])
def show_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', response_model=schema.ShowUser, tags=['User'])
def find_user(id: int, response:Response, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = 404, detail=f'User with id {id} is not available')
    return user

