from fastapi import APIRouter, Depends, status
from .. import schemes, database
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

get_db = database.get_db


@router.get('/{id}', response_model=schemes.User, status_code=200)
def show_user(id, db: Session = Depends(get_db)):
    return user.get(id, db)


@router.post("/", response_model=schemes.User, status_code=status.HTTP_201_CREATED)
def create_user(request: schemes.UserIn, db: Session = Depends(get_db)):
    return user.create(request, db)



