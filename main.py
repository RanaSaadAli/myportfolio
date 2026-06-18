from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.public import public
from routes.admin import admin
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(public)
app.include_router(admin)
app.include_router(admin, prefix="/admin")
