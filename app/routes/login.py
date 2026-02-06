from fastapi import APIRouter, Depends, HTTPException, Response
from app.models.user import User
from app.schemas.user_schema import user_schema
from app.dependencies.dependencies import getdb, verify_user_in_db
from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.services.auth import create_token, decrypt_password
load_dotenv()
router=APIRouter(
    prefix='/Auth',
    tags=['Auth']
)


context= CryptContext(schemes=["argon2"], deprecated="auto")

def decrypt_password(inserted_pasword: str, hashed_password: str):
    return context.verify(inserted_pasword, hashed_password)

@router.post('/login')
def login(user: user_schema, response:Response, db:Session= Depends(getdb)):
          user_db= db.query(User).filter(User.email == user.email).first()  
          print('test')
          user_db= db.query(User).filter(User.email == user.email).first()
          print('test')
          if not user_db:
             raise HTTPException(status_code=400, detail='user not exist')
          if not decrypt_password(user.hashedpassword, user_db.hashedpassword):
              raise HTTPException(status_code=401, detail='wrong password')
          token = create_token(user_db.email, user_db.id)
          response.set_cookie(
               key='token',
               value= token,
               httponly=True,
               secure=True,     
               samesite="None",
               path="/" 
          )
          return {'message': 'login succesfully!'}