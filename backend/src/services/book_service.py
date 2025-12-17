from .. import models, schemas
from sqlalchemy.orm import Session


def get_books(db: Session, genre: schemas.GenreEnum = None):
    """
    Pobiera wszyskie ksiązki z bazy danych lub tylko te z danego gatunku
    :param genre: gatunek po którym będzie filtrowanie
    :param db: sesja bazy danych
    """
    query = db.query(models.BookDB)
    if genre:
        query = query.join(models.BookDB.genres).filter(models.GenreDB.name == genre.value)
    return query.all()

def get_book_by_id(db: Session, book_id: int):
    """
    Pobiera książke po jej ID
    """
    return db.query(models.BookDB).filter(models.BookDB.id == book_id).first()

def create_book(db: Session, book: schemas.BookCreate):
    """
    Dodaje nową książke do bazy danych
    """
    book_data = book.dict(exclude={"genres"})
    db_book = models.BookDB(**book_data)

    if book.genres:
        db_book.genres = __get_or_create_genres(db, book.genres)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    """
    Aktualizuje istniejącą książke
    """
    db_book = db.query(models.BookDB).filter(models.BookDB.id == book_id).first()
    if db_book:
        db_book.title = book_update.title
        db_book.author = book_update.author
        db_book.description = book_update.description
        db_book.year_published = book_update.year_published
        db_book.pages = book_update.pages

        if book_update.genres is not None:
            db_book.genres = __get_or_create_genres(db, book_update.genres)

        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    """
    Usuwa książke po jej ID
    """
    db_book = db.query(models.BookDB).filter(models.BookDB.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def count_books(db: Session) -> int:
    """
    Zwraca liczbę książek w systemie
    """
    return db.query(models.BookDB).count()

def __get_or_create_genres(db: Session, genre_enums: list[schemas.GenreEnum]):
    """
    Zwraca listę gatunków na podstawie enuma i dodaje je do bazy danych
    """
    genres_db = []
    for genre_enum in genre_enums:
        name = genre_enum.value
        genre = db.query(models.GenreDB).filter(models.GenreDB.name == name).first()
        if not genre:
            genre = models.GenreDB(name=name)
            db.add(genre)
            db.commit()
            db.refresh(genre)
        genres_db.append(genre)
    return genres_db