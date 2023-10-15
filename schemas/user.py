from pydantic import BaseModel, Field


class User(BaseModel):
    email : str = Field(default="admin@mail.com")
    username: str
    password: str = Field(default="admin")