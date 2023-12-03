from .database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)

    creator = relationship("Blog", back_populates="blogs")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("User", back_populates="owner")