from typing import Annotated, Sequence
from uuid import UUID
from fastapi import FastAPI, Query, HTTPException, File, UploadFile, Form, status
from fastapi.staticfiles import StaticFiles
import shutil

# from app.schemas import PostCreate, PostResponse
from app.db import create_db_and_tables, Post, SessionDep
from contextlib import asynccontextmanager
from sqlmodel import select, col


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload")
def upload_file(
    session: SessionDep,
    file: UploadFile = File(...),
    caption: str = Form(...),
) -> Post:
    file_location = f"static/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    post = Post(
        caption=caption,
        url=f"/static/{file.filename}",
        file_type=file.content_type,
        file_name=file.filename,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@app.get("/feed")
def get_all_feed(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
) -> Sequence[Post]:
    feed = session.exec(
        select(Post).order_by(col(Post.created_at).desc()).offset(offset).limit(limit)
    ).all()
    return feed


@app.get("/feed/{post_id}")
def get_feed(post_id: UUID, session: SessionDep) -> Post:
    feed = session.get(Post, post_id)
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feed with id {post_id} not found",
        )
    return feed


@app.delete("/feed/{post_id}")
def delete_feed(post_id: UUID, session: SessionDep) -> None:
    feed = session.get(Post, post_id)
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feed with id {post_id} not found",
        )
    session.delete(feed)
    session.commit()
    return None
