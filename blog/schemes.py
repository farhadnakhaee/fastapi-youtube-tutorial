from pydantic import BaseModel, SecretStr

class BlogBase(BaseModel):
    title: str
    body: str

class BlogCreate(Blog):
    pass

class Blog(Blog):
    id: int
    owner_id: int

    class Config():
        orm_mode = True

class UserBase(BaseModel):
    name: str | None = None
    email: str | None = None
    
class UserIn(User):
    password: str | None = None
    
class User(User):
    id: int
    is_active: bool
    items: list[Blog] = []
