import os
from fastapi import HTTPException
from app.models.user import users
import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
load_dotenv()

def create_token(email, id):
    payload={
           "email" :email,
           "id": id
    }
    return jwt.encode(payload, os.getenv("JWT"), algorithm="HS256")



def decode_token(token: str):
    payload= jwt.decode(token , os.getenv("jwt_secret"), algorithms=os.getenv("ALGORITHM"))
    if payload:
       return payload

context= CryptContext(schemes='argon2', deprecated="auto")
def decrypt_password(inserted_password, hash_password):
    return context.verify(inserted_password, hash_password)