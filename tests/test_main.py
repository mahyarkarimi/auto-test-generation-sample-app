import pytest
from fastapi.testclient import TestClient
from main import app, Book

client = TestClient(app)

# Test data
initial_books = [
    {"id": 1, "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "description": "A comedy science fiction series."},
    {"id": 2, "title": "Pride and Prejudice", "author": "Jane Austen", "description": None}
]

@pytest.pytest.fixture(autouse=True)
def setup_database():
    # Clear and populate books for each test
    app.books.clear()
    for book_data in initial_books:
        app.books.append(Book(**book_data))
    yield

def test_read_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == len(initial_books)

def test_read_book_by_id_existing():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "description": "A comedy science fiction series."
    }

def test_read_book_by_id_non_existing():
    response = client.get("/books/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_create_book():
    new_book = {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "description": "A dystopian social science fiction novel."
    }
    response = client.post("/books", json=new_book)
    assert response.status_code == 201
    assert response.json() == new_book
    assert len(app.books) == len(initial_books) + 1

def test_create_book_missing_required_fields():
    # Test creating a book with missing title and author (if author were required)
    # Note: Based on the diff, author is now optional, so this test might need adjustment
    # If author is meant to be required, this test should fail for missing author.
    # test_data = {"id": 3, "description": "A test description"}
    # response = client.post("/books", json=test_data)
    # assert response.status_code == 422 # Or appropriate validation error code

    # Test creating a book with missing ID (which is always required)
    test_data = {"title": "Incomplete", "author": "Unknown"}
    response = client.post("/books", json=test_data)
    assert response.status_code == 422 # Pydantic validation error for missing 'id'

def test_create_book_with_optional_author_none():
    # Test creating a book where author is explicitly None, which should be valid per the diff
    new_book = {
        "id": 4,
        "title": "Book With No Author",
        "author": None,
        "description": "This book has no listed author."
    }
    response = client.post("/books", json=new_book)
    assert response.status_code == 201
    assert response.json() == new_book
    assert len(app.books) == len(initial_books) + 1

def test_update_book():
    update_data = {
        "title": "Updated Hitchhiker's Guide",
        "author": "Douglas Adams",
        "description": "An updated description."
    }
    response = client.put("/books/1", json=update_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Updated Hitchhiker's Guide",
        "author": "Douglas Adams",
        "description": "An updated description."
    }

def test_update_book_non_existing():
    update_data = {"title": "Non Existent Update"}
    response = client.put("/books/99", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_update_book_partial_update_optional_fields():
    # Test updating only the description
    update_data = {"description": "Only description updated."}
    response = client.put("/books/2", json=update_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "description": "Only description updated."
    }

def test_update_book_setting_optional_author_to_none():
    # Test updating a book and setting its optional author to None
    update_data = {"author": None}
    response = client.put("/books/1", json=update_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": None,
        "description": "A comedy science fiction series."
    }

def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}
    assert len(app.books) == len(initial_books) - 1

def test_delete_book_non_existing():
    response = client.delete("/books/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_delete_book_removes_from_list():
    client.delete("/books/1")
    response = client.get("/books/1")
    assert response.status_code == 404
