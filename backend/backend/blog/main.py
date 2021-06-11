from fastapi import FastAPI

from .schemas import Blog
from .models import Base
from ..core.database import engine

app = FastAPI()


@app.post("/blog")
def create(request: Blog):
    return "creating"
