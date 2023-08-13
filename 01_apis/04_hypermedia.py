from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List


app = FastAPI()


class Book(BaseModel):
    title: str
    author: str


books = []


@app.post("/books/", response_model=Book)
async def create_book_with_links(book: Book):
    books.append(book)
    book_id = len(books) - 1
    links = {
        "self": f"/books/{book_id}",
        "all_books": "/books/"
    }
    book.links = links  # Attach links to the book object
    return JSONResponse(content=book.dict())


@app.get("/books/", response_model=List[Book])
async def get_books_with_links():
    books_with_links = []
    for index, book in enumerate(books):
        links = {
            "self": f"/books/{index}",
            "all_books": "/books/"
        }
        book.links = links
        books_with_links.append(book)
    return books_with_links


@app.get("/books/{book_id}", response_model=Book)
async def get_book_with_links(book_id: int):
    if 0 <= book_id < len(books):
        book = books[book_id]
        links = {
            "self": f"/books/{book_id}",
            "all_books": "/books/"
        }
        book.links = links
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)