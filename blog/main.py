from fastapi import FastAPI, Depends, HTTPException, status
from . import schemes, models
from .database import engin, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engin)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(blog: schemes.CreateBlog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
 
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemes.ShowBlog], status_code=200, tags=['blogs'])
def read_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', response_model=schemes.ShowBlog, status_code=200, tags=['blogs'])
def read_one(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with the id {id} is not available.")
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemes.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id {id} not found.")
    blog.update(request.model_dump())
    db.commit()
    return 'updated'

@app.post("/users", response_model=schemes.UserOut, status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(user: schemes.UserIn, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=schemes.UserOut, status_code=200, tags=['users'])
def show_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} is not available.")
    return user

# ========================================================

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def fake_hash_password(password: str):
#     return "fakehashed" + password

# def get_user(username: str, db: Session = Depends(get_db)):
#     users = db.query(models.User)
#     if username in users:
#         user_dict = users[username]
#         return schemes.UserIn(**user_dict)

# def fake_decode_token(token):
#     user = get_user(???, token)
#     return user

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user

# @app.get('/users/', status_code=200)
# def show_user(current_user: Annotated[schemes.User, Depends(get_current_user)]):
#     return current_user 