
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from ..schemas.user_schema import user_schema
from app.dependencies.dependencies import getdb
from app.models.user import users
from passlib.context import CryptContext

router= APIRouter(
         prefix="/history",
         tags= ["history"]
)

@router.post('/history')
def register(db:Session= Depends(getdb)):
   
    return "hi"