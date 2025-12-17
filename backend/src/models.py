from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from .database import Base


book_genres = Table(
    'book_genres',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class GenreDB(Base):
    """
    Klasa encji dla tabeli genres
    """
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    books = relationship("BookDB", secondary=book_genres, back_populates="genres")

class BookDB(Base):
    """
    Klasa encji dla tabeli books
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), index=True)
    author = Column(String(100))
    description = Column(Text)
    year_published = Column(Integer)
    pages = Column(Integer)
    reviews = relationship("ReviewDB", back_populates="book", cascade="all, delete-orphan")
    genres = relationship("GenreDB", secondary=book_genres, back_populates="books")

class ReviewDB(Base):
    """
    Klasa encji dla tabeli reviews
    """
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment = Column(Text)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("BookDB", back_populates="reviews")