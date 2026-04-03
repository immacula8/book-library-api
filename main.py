# main.py - Complete Book Library API

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError

# Import our modules
from database import get_db, engine
from models import Base, BookDB
from schemas import BookCreate, Book

# Create database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Book Library API", version="2.0.0")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# ==================== WELCOME ENDPOINT ====================
@app.get("/")
def read_root():
    """Welcome message"""
    return {"message": "Welcome to the Book Library API!"}

# ==================== GET ALL BOOKS ====================
@app.get("/books", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    """Get all books from database"""
    books = db.query(BookDB).all()
    return books

# ==================== SEARCH BOOKS ====================
# IMPORTANT: This MUST come BEFORE /books/{book_id}
@app.get("/books/search", response_model=List[Book])
def search_books(
    title: str = None,
    author: str = None,
    db: Session = Depends(get_db)
):
    """
    Search for books by title or author.
    
    Examples:
    - /books/search?title=great
    - /books/search?author=orwell
    - /books/search?title=great&author=fitzgerald
    """
    # Start with all books
    query = db.query(BookDB)
    
    # If user wants to search by title
    if title:
        query = query.filter(BookDB.title.ilike(f"%{title}%"))
    
    # If user wants to search by author
    if author:
        query = query.filter(BookDB.author.ilike(f"%{author}%"))
    
    # Get and return the results
    return query.all()

# ==================== GET ONE BOOK ====================
@app.get("/books/{book_id}", response_model=Book)
def get_one_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    return book

# ==================== CREATE BOOK ====================
@app.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book (prevents duplicates)"""
    
    # First, check if this exact book already exists
    existing_book = db.query(BookDB).filter(
        BookDB.title == book.title,
        BookDB.author == book.author,
        BookDB.year == book.year
    ).first()
    
    # If it exists, return a friendly error message
    if existing_book:
        raise HTTPException(
            status_code=400,
            detail=f"Book '{book.title}' by {book.author} ({book.year}) already exists in the library!"
        )
    
    # If it doesn't exist, create the new book
    db_book = BookDB(
        title=book.title,
        author=book.author,
        year=book.year
    )
    
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        # This is a backup check in case the database constraint catches something
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Book '{book.title}' by {book.author} ({book.year}) already exists!"
        )
# ==================== UPDATE BOOK ====================
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """Update an existing book"""
    # Find the book
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    # Update the fields
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
    
    # Save changes
    db.commit()
    db.refresh(db_book)
    
    return db_book

# ==================== DELETE BOOK ====================
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    # Find the book
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    # Delete it
    db.delete(db_book)
    db.commit()
    
    return {"message": f"Book {book_id} deleted successfully"}