from fastapi import FastAPI

app = FastAPI()

from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None

books: List[Book] = []


# List all books
@app.get("/books", response_model=List[Book])
def list_books():
    return books



# Get a book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}

# Create a new book
@app.post("/books", response_model=Book)
def create_book(book: Book):
    books.append(book)
    return book

# Update a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for idx, book in enumerate(books):
        if book.id == book_id:
            books[idx] = updated_book
            return updated_book
    return {"error": "Book not found"}

# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for idx, book in enumerate(books):
        if book.id == book_id:
            deleted = books.pop(idx)
            return {"message": "Book deleted", "book": deleted}
    return {"error": "Book not found"}