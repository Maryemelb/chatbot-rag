from fastapi import FastAPI
from app.routes.login import router as login_router
from app.routes.register import router as register_router
from sqlalchemy_utils import create_database, database_exists
from app.db.database import Base, engine
from app.schemas import user_schema
app= FastAPI()
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(bind= engine)

app.include_router(register_router)
app.include_router(login_router)
