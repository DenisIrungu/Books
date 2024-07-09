from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
import model
from sqlalchemy.orm import session


app = FastAPI()

model.Base.metadata.create_all(bind=engine)


class BookBase(BaseModel):
    id: int
    title: str 
    author: str 
    description: str 
    rating: int 

def get_db():
    db=SessionLocal ()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[session, Depends(get_db)]

@app.post("/books/")
async def create_book(book:BookBase, db: db_dependency):
    db_book= model.Book(**book.dict())
    db.add(db_book)
    db.commit()

@app.get("/books/{book_id}", status_code= status.HTTP_200_OK)
async def read_books(book_id: int, db:db_dependency):
    book = db.query(model.Book).filter(model.Book.id==book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail= "Book not found")
    return book

@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id:int, db:db_dependency):
    book=db.query(model.Book).filter(model.Book.id==book_id).first()
    db.delete(book)
    db.commit()

# BOOKS= []

# @app. get("/")
# async def read_api():
#     return BOOKS

# @app.post("/")
# async def create_book(book:Book):
#     BOOKS.append(book)
#     return book

# @app.put("/{book_id}")
# async def update_book(book_id:UUID, book: Book):
#     counter = 0
#     for x in BOOKS:
#         counter+=1
#         if x.id == book_id:
#             BOOKS[counter-1]=book
#         return BOOKS[counter-1]
#     raise HTTPException(
#         status_code= 404,
#         detail= f"ID {book_id}: Does no exist")

# @app.delete("/{book_id}")
# async def delete_book(book_id: UUID):
#     counter = 0
#     for x in BOOKS:
#         counter +=1
#         if x.id==book_id:
#             del BOOKS[counter-1]
#             return f"ID:{book_id} deleted"
#     raise HTTPException(status_code=404, 
#                             detail= f"ID {book_id}: Does not exist")
    




