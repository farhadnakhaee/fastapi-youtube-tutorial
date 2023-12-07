from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class BlogCreate(BlogBase):
    user_id: int


class UserBase(BaseModel):
    name: str | None = None
    email: str | None = None


class UserIn(UserBase):
    password: str | None = None


class User(BaseModel):
    name: str
    email: str
    blogs: list[BlogBase]

    class Config:
        orm_mode = True


class Blog(BaseModel):
    title: str
    body: str
    creator: UserBase

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

