from sqlalchemy import Column, String, Integer
from app.db.database import Base

class Question(Base):
    __tablename__= "Question"
    id= Column(Integer, primary_key=True)
    question= Column(String)
