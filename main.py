import uvicorn
from fastapi import FastAPI

from db import models
from db.database import engine, get_db
from routes.auth import router as RouterAuth
from routes.posts import router as RouterPost
from routes.users import router as RouterUser
from routes.votes import router as RouterVote

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Demo",
    docs_url="/",
    description="This is a very fancy project, with auto docs for the API and everything",
)

get_db()


app.include_router(RouterPost)
app.include_router(RouterUser)
app.include_router(RouterAuth)
app.include_router(RouterVote)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)
