from sqlalchemy import Column, Integer, String, UniqueConstraint
from database import Base

class BookDB(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    
    # Prevents duplicate books (same title, author, and year)
    __table_args__ = (
        UniqueConstraint('title', 'author', 'year', name='unique_book'),
    )