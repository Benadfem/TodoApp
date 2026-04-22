from fastapi import FastAPI

import models
from database import engine
from routers import auth, todos, admin

app = FastAPI()


"""
fastapi will automatically create a database for the applicaiton 
since there is model an database connection creation 
"""
models.Base.metadata.create_all(engine)

"""
to see the router from the router package
"""
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)