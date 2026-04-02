# models.py - Defines what a book looks like in the database

from sqlalchemy import Column, Integer, String
from database import Base

# Define the Book table structure
class BookDB(Base):
    __tablename__ = "books"  # Name of the table in database
    
    # Define columns (fields) in the table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)