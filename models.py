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


class Book(BaseModel):
    url = peewee.TextField(null=False, verbose_name='Link')
    title = peewee.CharField(max_length=255, null=False, verbose_name='Title')
    author = peewee.ForeignKeyField(model=Author, null=False)
    rate = peewee.FloatField(null=False, verbose_name='Rate')

    class Meta:
        database = main.database_manager.db

    def __str__(self) -> str:
        """Override str method"""
        return f'{self.title}'


class BookGenre(BaseModel):
    book = peewee.ForeignKeyField(model=Book, verbose_name='Book')
    genre = peewee.ForeignKeyField(model=Genre, verbose_name='Genre')

    class Meta:
        database = main.database_manager.db

    def __str__(self):
        """Override str method"""
        return f'{self.book} : {self.genre}'


class Keyword(BaseModel):
    keyword = peewee.CharField(max_length=255, null=False, verbose_name='Keyword')

    class Meta:
        database = main.database_manager.db

    def __str__(self):
        """Override str method"""
        return self.keyword


class SearchByKeyword(BaseModel):
    keyword = peewee.ForeignKeyField(model=Keyword, on_delete='CASCADE', verbose_name='Keyword')
    search_type = peewee.CharField(max_length=255, null=False, verbose_name='Search Type')
    search_tab = peewee.CharField(max_length=255, default=search_type, verbose_name='Search Tab')
    page_count = peewee.IntegerField(null=False, verbose_name='Page Count')

    class Meta:
        database = main.database_manager.db

    def __str__(self):
        """Override str method"""
        return f'{self.keyword} {self.search_type} {self.page_count} pages'
