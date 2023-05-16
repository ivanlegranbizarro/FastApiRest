from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    posts = relationship("Post", back_populates="author")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()"
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()"
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    published = Column(Boolean, server_default="True")
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User", back_populates="posts")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()"
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()"
    )
    votes = relationship("Vote", back_populates="post")


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    post = relationship("Post", back_populates="votes")
