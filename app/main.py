from fastapi import FastAPI
from app.routes.login import router as login_router
from app.routes.register import router as register_router
from sqlalchemy_utils import create_database, database_exists
from app.db.database import Base, engine
from app.schemas import user_schema
from app.models.question import Question
from app.db.database import questions_list, sessionLocal
app= FastAPI()

if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    
    db = sessionLocal()
    try:
        for q in questions_list:
            question = Question(question=q)
            db.add(question)
        
        db.commit()
        print("Successfully seeded questions_list into the database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()
else:
    Base.metadata.create_all(bind=engine)

app.include_router(register_router)
app.include_router(login_router)
