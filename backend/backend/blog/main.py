from fastapi import FastAPI

from .routers import blog, user, auth


app = FastAPI()

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)
