from .. import schemes, models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def create(blog: schemes.BlogCreate, db: Session):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=blog.user_id)
    db.add(new_blog)
    db.commit()

    db.refresh(new_blog)
    return new_blog


def get_one(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available.")
    return blog


def delete(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


def update(id, request: schemes.BlogBase, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found.")
    blog.update(request.model_dump())
    db.commit()
    return 'updated'
