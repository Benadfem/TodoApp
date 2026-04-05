from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

"""
fastapi will automatically create a database for the applicaiton 
since there is model an database connection creation 
"""
models.Base.metadata.create_all(engine)

