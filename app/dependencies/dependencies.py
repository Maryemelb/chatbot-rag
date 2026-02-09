


from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from grpc import Status
from requests import Session
from app.db.database import sessionLocal
from app.models.user import User
import chromadb
from chromadb.config import Settings
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from fastapi import status
load_dotenv()
import jwt
def getdb():
    db = sessionLocal()     
    try:
      yield db
    finally:
      db.close()

def verify_user_in_db(user_in_token: str, db):
    user_in_db= db.query(User).filter(User.email == user_in_token).first()
    if not user_in_db:
       raise HTTPException(status_code=404, detail="Token not valid")
    return user_in_db.email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(request: Request, db: Session = Depends(getdb)):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(token, key=os.getenv("JWT"), algorithms=["HS256"])
        user_id = payload.get("id")
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

embedding= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db_path = os.getenv("CHROMA_PATH", "./core/dataset/chroma_data2")
# Initialize the PersistentClient
client = chromadb.PersistentClient(
    path=db_path,
    settings=Settings(allow_reset=True)
)