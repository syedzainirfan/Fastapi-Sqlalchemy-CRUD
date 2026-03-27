from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


# DATABASE
DATABASE_URL = "postgresql://postgres:1234@localhost/Fastapi"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

var1 = FastAPI()


# MODEL
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


# SCHEMA
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


# UPDATE ONLY
@var1.put("/post/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    query = db.query(Posts).filter(Posts.id == id)
    db_post = query.first()

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"DATA": query.first()}
