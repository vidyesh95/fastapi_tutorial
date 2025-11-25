from uuid import UUID, uuid7
from typing import Annotated
from fastapi import Depends

from sqlmodel import Field, Session, SQLModel, create_engine


class Post(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    title: str = Field(index=True, max_length=100)
    content: str = Field(max_length=1000)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
