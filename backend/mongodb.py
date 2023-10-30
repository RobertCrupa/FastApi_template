from __future__ import annotations

from mongoengine import connect
from mongoengine import Document
from mongoengine import FloatField
from mongoengine import IntField
from mongoengine import ListField
from mongoengine import StringField

connect('mongoengine_test', host='localhost', port=27017)


class Books(Document):
    title = StringField(max_length=200, required=True)
    author = StringField(max_length=50, required=True)
    contributors = ListField(StringField(max_length=50))
    price = FloatField(required=True)
    pages = IntField(required=True)


# Create a few book objects
book1 = Books(
    title='The Pragmatic Programmer',
    author='Andy Hunt',
    contributors=['Dave Thomas', 'Mike Clark'],
    pages=352,
    price=36.99,
)

book1.save()  # Insert the document under the books collection

book2 = Books(
    title='Head First Python',
    author='Paul Barry',
    contributors=['Jason Briggs'],
    pages=494,
    price=54.99,
)

book2.save()
