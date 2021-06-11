from typing import Optional
from fastapi import FastAPI

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


app = FastAPI()


@app.get("/blog")
def index(limit: int = 0, sort: Optional[str] = None):
    return {"data": f"{limit} blog list"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": {"all"}}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": {"id": id}}


@app.get("/blog/{id}/comments/")
def comments(id):
    return {"data": {"1", "2"}}


@app.post("/blog")
def create_blog(request: Blog):
    return {"data": f"Blog is created with title {request.title}"}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="127.0.0.1", port=9000)
