from fastapi import Depends
from sqlalchemy.orm.session import Session
from .. import schema, models, database
from fastapi.exceptions import HTTPException
from ..hashing import Hash

def create(request: schema.User, db: Session ):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


def find(id: int, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = 404, detail=f'User with id {id} is not available')
    return user