
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from ..schemas.user_schema import user_schema
from app.dependencies.dependencies import getdb
from app.models.user import User
from passlib.context import CryptContext

router= APIRouter(
         prefix="/health",
         tags= ["health"]
)

@router.post('/')
def health():
    return "hello backend is working"