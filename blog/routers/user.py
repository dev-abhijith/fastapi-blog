from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from .. import schema, database
from typing import List
from ..repositories import user

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/', status_code=201)
def create_user(request: schema.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get('/', response_model=List[schema.ShowUser])
def show_users(db: Session = Depends(database.get_db)):
    return user.show(db)


@router.get('/{id}', response_model=schema.ShowUser)
def find_user(id: int, db:Session = Depends(database.get_db)):
    return user.find(id, db)

