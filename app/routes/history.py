
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from ..schemas.user_schema import user_schema
from app.dependencies.dependencies import getdb
from passlib.context import CryptContext

router= APIRouter(
         tags= ["history"]
)

@router.post('/history')
def history(db:Session= Depends(getdb)):
     
    return "hi"