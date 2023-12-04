from fastapi import APIRouter, Depends, status
from .. import schemes, models, database
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)
get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemes.BlogCreate, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.get('/', response_model=list[schemes.Blog], status_code=200)
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@router.get('/{id}', response_model=schemes.Blog, status_code=200)
def get_one(id, db: Session = Depends(get_db)):
    return blog.get_one(id, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemes.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)
