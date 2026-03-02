# Book Listing API Requirements

This API is for testing purposes only and provides CRUD operations for managing a list of books.

## Functional Requirements

- List all books
- Retrieve a book by its ID
- Create a new book
- Update an existing book
- Delete a book

## Technical Requirements

- Use FastAPI for building the API
- Use Pydantic models for request/response validation
- Store books in an in-memory list (no database required)
- Each book should have:
  - `id` (integer)
  - `title` (string)
  - `author` (string)
  - `description` (optional string)

## Endpoints

- `GET /books` — List all books
- `GET /books/{book_id}` — Get a book by ID
- `POST /books` — Create a new book
- `PUT /books/{book_id}` — Update a book
- `DELETE /books/{book_id}` — Delete a book

## Notes

- This API is for demonstration and testing only. Data is not persisted.
