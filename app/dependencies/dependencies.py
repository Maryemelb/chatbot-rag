


from fastapi import HTTPException
from app.db.database import sessionLocal
from app.models.user import users
from langchain_community.embeddings import HuggingFaceEmbeddings


def getdb():
    db = sessionLocal()     
    try:
      yield db
    finally:
      db.close()

def verify_user_in_db(user_in_token: str, db):
    user_in_db= db.query(users).filter(users.email == user_in_token).first()
    if not user_in_db:
       raise HTTPException(status_code=404, detail="Token not valid")
    return user_in_db.email


embedding= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

