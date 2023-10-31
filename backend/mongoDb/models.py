from __future__ import annotations

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type='string')


class Book(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    title: str = Field(max_length=200, min_length=1, required=True)
    author: str = Field(max_length=50, required=True)
    contributors: str = Field(max_length=50)
    price: float = Field(required=True)
    pages: int = Field(required=True)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            'example': {
                'title': 'The Pragmatic Programmer',
                'author': 'Andy Hunt',
                'contributors': ['Dave Thomas', 'Mike Clark'],
                'pages': 352,
                'price': 36.99,
            },
        }


class UpdateBookModel(BaseModel):
    title: str | None
    author: str | None
    contributors: list[str] | None
    price: float | None
    pages: int | None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            'example': {
                'title': 'Head First Python',
                'author': 'Paul Barry',
                'contributors': ['Jason Briggs'],
                'pages': '494',
                'price': '54.99',
            },
        }


def generate_books():
    # Create a few book objects
    book1 = Book(
        title='The Pragmatic Programmer',
        author='Andy Hunt',
        contributors=['Dave Thomas', 'Mike Clark'],
        pages=352,
        price=36.99,
    )

    book1.save()  # Insert the document under the books collection

    book2 = Book(
        title='Head First Python',
        author='Paul Barry',
        contributors=['Jason Briggs'],
        pages=494,
        price=54.99,
    )

    book2.save()
