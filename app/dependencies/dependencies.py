


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

def get_current_user (request: Request, db: Session = Depends(getdb)):
    token = request.cookies.get("token")
    if token is None:
        raise HTTPException(
            status_code=Status.HTTP_401_UNAUTHORIZED, 
            detail="Token d'authentification manquant dans le header"
        )
    try :
       payload = jwt.decode(token,key=os.getenv('JWT'),algorithms="HS256")
       user_id = payload.get("id")
       if user_id is None:
           raise HTTPException(status_code=403, detail="Token invalide : ID utilisateur absent")
       
    except:
      raise HTTPException(status_code=401,detail="Token expiré ou corrompu")

    user_db = db.query(User).filter(User.id == user_id).first()
    
    
    if not user_db:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user_db


embedding= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db_path = os.getenv("CHROMA_PATH", "./core/dataset/chroma_data2")
# Initialize the PersistentClient
client = chromadb.PersistentClient(
    path=db_path,
    settings=Settings(allow_reset=True)
)