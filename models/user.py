from config.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy import Float, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password  = Column(String)