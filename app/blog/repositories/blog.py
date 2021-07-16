
from sqlalchemy.orm.session import Session
from .. import schema, models
from fastapi.exceptions import HTTPException

def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, db:Session):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted'


def update(id: int, request: schema.Blog,  db: Session ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= 404, detail=f'the post with id {id} not found')
    else:
        blog.update({'title': request.title, 'body': request.body},synchronize_session=False)
    db.commit()
    return 'Updated'


def show(id: int, db:Session ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = 404, detail=f'blog with id {id} is not available')
    return blog