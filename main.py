from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import HTTPException
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": " Welcome to the Book Library API!"}

books = []

@app.get("/books")
def get_books():
    return {"books": books}

class Book(BaseModel):
    title: str
    author: str
    year: int

@app.post("/books")
def create_books(book: Book):
    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "author": book.author,
        "year": book.year
    }
    books.append(new_book)
    return new_book

@app.get("/books/{book_id}")
def get_one_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    
    for index, existing_book in enumerate(books):
        if existing_book["id"] == book_id:
            
            books[index] = {
                "id": book_id,
                "title": book.title,
                "author": book.author,
                "year": book.year
            }

            return books[index]
    
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    
    for index, existing_book in enumerate(books):
        if existing_book["id"] == book_id:
            books.pop(index)
            return {"message": f"Book {book_id} deleted successfully"}
    
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")