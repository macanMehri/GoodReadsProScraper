import peewee
from datetime import datetime
import main


class BaseModel(peewee.Model):
    created_date = peewee.DateTimeField(default=datetime.now())

    class Meta:
        abstract = True

    def __str__(self):
        raise NotImplementedError('Str method should be overridden!')


class Genre(BaseModel):
    title = peewee.CharField(max_length=255, null=False, verbose_name='Title')

    class Meta:
        database = main.database_manager.db

    def __str__(self):
        """Override str method"""
        return self.title


class Author(BaseModel):
    name = peewee.CharField(max_length=255, null=False, verbose_name='Name')
    books = peewee.IntegerField(null=False, verbose_name='Number Of Books')
    followers = peewee.CharField(max_length=255, null=False, verbose_name='Number Of Followers')

    class Meta:
        database = main.database_manager.db

    def __str__(self) -> str:
        """Override str method"""
        return f'{self.name} followed by {self.followers} and written {self.books} books'


class Edition(BaseModel):
    edition_format = peewee.CharField(max_length=255, null=False, verbose_name='Edition Format')
    edition_published_date = peewee.CharField(max_length=255, null=False, verbose_name='Edition Published Date')
    isbn = peewee.CharField(max_length=255, null=False, verbose_name='ISBN')
    language = peewee.CharField(max_length=255, null=False, verbose_name='Language')

    class Meta:
        database = main.database_manager.db

    def __str__(self) -> str:
        """Override str method"""
        return f'{self.isbn}'


class Book(BaseModel):
    url = peewee.TextField(null=False, verbose_name='Link')
    title = peewee.CharField(max_length=255, null=False, verbose_name='Title')
    author = peewee.ForeignKeyField(model=Author, null=False)
    rate = peewee.CharField(max_length=255, null=False, verbose_name='Rate')
    first_published_date = peewee.CharField(max_length=255, null=False, verbose_name='First Published Date')

    class Meta:
        database = main.database_manager.db

    def __str__(self) -> str:
        """Override str method"""
        return f'{self.title}'
