from typing import Annotated, Sequence
from fastapi import FastAPI, Query, HTTPException, File, UploadFile, Form, status

# from app.schemas import PostCreate, PostResponse
from app.db import create_db_and_tables, Post, SessionDep
from contextlib import asynccontextmanager
from sqlmodel import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# text_posts = {
#     1: {
#         "title": "New Post",
#         "content": "Lorem ipsum Bug Catcher traveled from Goldenrod City to Ilex Forest via Route 34.Lorem ipsum You can find the Azalea Gym in Johto.",
#     },
#     2: {
#         "title": "Old Post",
#         "content": "Lorem ipsum Kindler journeyed along Route 9 between Route 10 and Cerulean City.",
#     },
#     3: {
#         "title": "New Post",
#         "content": "Lorem ipsum Bug Catcher traveled from Goldenrod City to Ilex Forest via Route 34.",
#     },
#     4: {
#         "title": "New Post",
#         "content": "Lorem ipsum Team Plasma's favorite Pokémon is Snorlax.",
#     },
#     5: {
#         "title": "Old Post",
#         "content": "Lorem ipsum You can earn the Soul Badge at Fuchsia Gym.",
#     },
#     6: {
#         "title": "New Post",
#         "content": "Lorem ipsum Hoopster spotted Butterfree in Kalos.",
#     },
#     7: {"title": "New Post", "content": "Lorem ipsum Metapod evolved into Butterfree."},
#     8: {"title": "New Post", "content": "Lorem ipsum Omanyte evolved into Omastar."},
#     9: {
#         "title": "New Post",
#         "content": "Lorem ipsum You can earn the Fighting Badge at Stow-on-Side Stadium.",
#     },
#     10: {"title": "New Post", "content": "Lorem ipsum Machoke used Seismic Toss."},
# }


# @app.get("/posts")
# async def get_all_posts(limit: int | None = None):
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts


# @app.get("/posts/{post_id}")
# async def get_post(post_id: int):
#     if post_id not in text_posts:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {post_id} not found",
#         )
#     return text_posts.get(post_id)


# @app.post("/posts")
# async def create_post(post: PostCreate) -> PostResponse:
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post
#     return PostResponse(**new_post)

# @app.post("/posts")
# async def create_post(post_id: int, post: PostCreate) -> PostResponse:
#     if post_id in text_posts:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Post with id {post_id} already exists",
#         )
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[post_id] = new_post
#     return PostResponse(**new_post)


@app.post("/upload")
def upload_file(post: Post, session: SessionDep) -> Post:
    post = Post(
        caption=post.caption,
        url=post.url,
        file_type=post.file_type,
        file_name=post.file_name,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@app.get("/feeds")
def get_feed(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
) -> Sequence[Post]:
    feeds = session.exec(select(Post).offset(offset).limit(limit)).all()
    return feeds
