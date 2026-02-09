
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from ..schemas.user_schema import user_schema
from app.dependencies.dependencies import getdb
from passlib.context import CryptContext
from app.models.query import Query
from app.models.user import User
from app.dependencies.dependencies import get_current_user
router= APIRouter(
         tags= ["history"]
)
#query_schema:query_schema,  db:Session= Depends(getdb), 
@router.get('/history')
def history(db:Session= Depends(getdb),
            current_user: User = Depends(get_current_user)):
    query_history= db.query(Query).all()
    return query_history