
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from .. import schema, database
from typing import List
from ..repositories import blog


router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/', response_model=List[schema.ShowBlog])
def all(db:Session = Depends(database.get_db)):
    return blog.get_all(db)


@router.post('/', status_code=201)  
def create(request: schema.Blog, db:Session = Depends(database.get_db)):
    return blog.create(request,db)
    


@router.delete('/{id}', status_code=204)
def delete(id: int, db:Session = Depends(database.get_db)):
    return blog.delete(id, db)


@router.put('/{id}', status_code= 202)
def update(id: int, request: schema.Blog,  db: Session = Depends(database.get_db)):
    return blog.update(id,request,db)
    

@router.get('/{id}', status_code=200, response_model=schema.ShowBlog)
def show(id: int, db:Session = Depends(database.get_db)):
    return blog.show(id,db)