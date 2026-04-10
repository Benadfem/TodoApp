from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
the line below holds the location of the database in the app directory 
"""
SQLALCHEMY_DATABASE_URI = 'sqlite:///./todosapp.db'


"""
The line below creates the link between python code and the database
software
"""
engine =  create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()