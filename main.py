from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Annotated

import models
from database import engine, SessionLocal

app = FastAPI()

"""
fastapi will automatically create a database for the applicaiton 
since there is model an database connection creation 
"""
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# let's create a variable db_dependency to hold the annotation
db_dependency =Annotated[Session,Depends(get_db)]
@app.get("/")
async def read_all(db: db_dependency):
    return db.query(models.Todos).all()
