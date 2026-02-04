
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from ..schemas.user_schema import user_schema
from app.dependencies.dependencies import getdb
from app.models.user import users
from passlib.context import CryptContext
from app.models.query import Query
from app.schemas.query_schema import query_schema
router= APIRouter(
         prefix="/query",
         tags= ["query"]
)

@router.post('/query')
def register(query_schema:query_schema,  db:Session= Depends(getdb)):
   
    return "hi"