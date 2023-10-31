from __future__ import annotations

from typing import List

from fastapi import Body
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from mongoDb import db
from mongoDb.models import Book
from mongoDb.models import UpdateBookModel

app = FastAPI()


@app.get(
    '/books/{id}',
    response_description='Get a single book', response_model=Book,
)
async def get_book(id: int):
    if (book := await db['books'].find_one({'id': id})) is not None:
        return book

    raise HTTPException(
        status_code=404,
        detail=f'Book {id} not found',
    )


@app.get(
    '/books',
    response_description='List all books', response_model=List[Book],
)
async def list_books():
    return await db['books'].find().to_list(1000)


@app.post(
    '/books',
    response_description='Add a new book',
    response_model=Book, status_code=status.HTTP_201_CREATED,
)
async def create_book(book: Book):
    book = jsonable_encoder(book)
    new_book = await db['books'].insert_one(book)
    created_book = await db['books'].find_one({'_id': new_book.inserted_id})

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=created_book,
    )


@app.put(
    '/books/{id}',
    response_description='Update a book', response_model=Book,
)
async def update_book(id: int, book: UpdateBookModel = Body(...)):
    book = {k: v for k, v in book.model_dump().items() if v is not None}

    if len(book) >= 1:
        update_result = await db['books'].update_one(
            {'_id': id},
            {'$set': book},
        )

        if update_result.modified_count == 1:
            if (
                    updated_book := await db['books'].find_one({'_id': id})
            ) is not None:
                return updated_book

    if (
            existing_book := await db['books'].find_one({'_id': id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=404, detail=f'Book {id} not found')


@app.delete('/books/{id}', response_description='Delete a book')
async def delete_book(id: int):
    delete_result = await db['books'].delete_one({'_id': id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Book {id} not found')


@app.get('/hello')
def hello():
    return {'hello': 'world'}
