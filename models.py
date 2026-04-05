from database import Base
from sqlalchemy import Column, Integer, String, Boolean


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