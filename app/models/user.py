from app.db.database import Base
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime

class users(Base):
    __tablename__= "users"
    id = Column(Integer,primary_key=True)
    email = Column(String, nullable=False)
    hashedpassword = Column(String, nullable=False)
    isactive = Column(Boolean, default= True)
    created_at = Column(DateTime, default= datetime.now )
    