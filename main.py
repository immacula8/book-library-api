# main.py - Complete API with SQLite database

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# Import our modules
from database import get_db, engine
from models import Base, BookDB
from schemas import BookCreate, Book

# Create database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Book Library API", version="2.0.0")

# Welcome endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Library API!"}

# Get all books
@app.get("/books", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    """Get all books from database"""
    books = db.query(BookDB).all()
    return books

# Get one book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_one_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    return book

# Create a new book
@app.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book"""
    # Create new database book
    db_book = BookDB(
        title=book.title,
        author=book.author,
        year=book.year
    )
    
    # Add to database and save
    db.add(db_book)
    db.commit()
    db.refresh(db_book)  # Get the auto-generated ID
    
    return db_book

# Update a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """Update an existing book"""
    # Find the book in database
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    # Update the book fields
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
    
    # Save to database
    db.commit()
    db.refresh(db_book)
    
    return db_book

# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    # Find the book in database
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    # Delete from database
    db.delete(db_book)
    db.commit()
    
    return {"message": f"Book {book_id} deleted successfully"}