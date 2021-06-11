from enum import unique

from sqlalchemy.sql.schema import ForeignKey
from ..core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    password = Column(String)
    email = Column(String)
    name = Column(String)
    blogs = relationship("Blog", back_populates="user")
