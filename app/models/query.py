
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from app.db.database import Base
import datetime
from sqlalchemy.orm import relationship


class Query(Base):
    __tablename__= "Query"
    id= Column(Integer, primary_key=True)
    question= Column(String)

    userid = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="queries")  
      
    question = Column(String)
    answer = Column(String)
    cluster = Column(Integer)
    latency_ms = Column(Float)
    created_at = Column(DateTime, default= datetime.now )
