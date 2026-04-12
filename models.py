from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

"""
let's create a class for the users model this is also called the schema
"""
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    roles = Column(String)


"""
created the class for the Todos model, identifying each attribute for 
"""
class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))