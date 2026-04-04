from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os

# Import our modules
from database import get_db, engine
from models import Base, BookDB
from schemas import BookCreate, Book

# Create database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Book Library API", version="2.0.0")

# Mount static files (CSS, JS, HTML assets if any)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== ROOT ENDPOINT - SERVES HTML INTERFACE ====================
@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the book library web interface"""
    html_path = os.path.join("static", "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Book Library API</h1><p>Static files not found. Visit <a href='/docs'>/docs</a> for API documentation.</p>")

# ==================== API ENDPOINTS ====================

# Get all books
@app.get("/books", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    """Get all books from database"""
    books = db.query(BookDB).all()
    return books

# Search books
@app.get("/books/search", response_model=List[Book])
def search_books(
    title: str = None,
    author: str = None,
    db: Session = Depends(get_db)
):
    """Search for books by title or author"""
    query = db.query(BookDB)
    
    if title:
        query = query.filter(BookDB.title.ilike(f"%{title}%"))
    
    if author:
        query = query.filter(BookDB.author.ilike(f"%{author}%"))
    
    return query.all()

# Get one book
@app.get("/books/{book_id}", response_model=Book)
def get_one_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    return book

# Create a book
@app.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book (prevents duplicates)"""
    
    # Check if book already exists
    existing_book = db.query(BookDB).filter(
        BookDB.title == book.title,
        BookDB.author == book.author,
        BookDB.year == book.year
    ).first()
    
    if existing_book:
        raise HTTPException(
            status_code=400,
            detail=f"Book '{book.title}' by {book.author} ({book.year}) already exists!"
        )
    
    db_book = BookDB(
        title=book.title,
        author=book.author,
        year=book.year
    )
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book

# Update a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """Update an existing book"""
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
    
    db.commit()
    db.refresh(db_book)
    
    return db_book

# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    db.delete(db_book)
    db.commit()
    
    return {"message": f"Book {book_id} deleted successfully"}