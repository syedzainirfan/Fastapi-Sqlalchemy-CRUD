from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


# DATABASE SETUP
DATABASE_URL = "postgresql://postgres:1234@localhost/Fastapi"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# FASTAPI APP
var1 = FastAPI()


# MODEL (TABLE)
class Posts(Base):
    __tablename__ = "new_posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )


# SCHEMA (REQUEST BODY)
class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


# DB DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE TABLE
Base.metadata.create_all(bind=engine)


# CREATE POST ONLY
@var1.post("/create/sqlalchemy")
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = Posts(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"DATA": new_post}
