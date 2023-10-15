from pydantic import BaseModel, Field 
from typing import Optional





class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="my movie",min_length=5, max_length=20)
    overview: str = Field(default="my movie",min_length=5, max_length=50)
    year: int = Field(default=2022, le=2023)
    rating: float = Field( ge=1, le=10.0)
    category: str = Field(default="my movie", min_length=5, max_length=20)