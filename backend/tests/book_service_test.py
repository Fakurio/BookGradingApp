import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.services import book_service
from src import schemas

@pytest.fixture(scope="function")
def db_session():
    """
    Tworzy nową bazę SQLite w pamięci dla każdego testu
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_book(db_session):
    book_in = schemas.BookCreate(
        title="Test Book",
        author="Test Author",
        description="A test description with enough length.",
        year_published=2023,
        pages=100,
        genres=[schemas.GenreEnum.FICTION]
    )
    book = book_service.create_book(db_session, book_in)

    assert book.id is not None
    assert book.title == "Test Book"
    assert len(book.genres) == 1
    assert book.genres[0].name == "Fiction"


def test_get_book_by_id(db_session):
    book_in = schemas.BookCreate(
        title="Find Me", author="Author", description="A test description with enough length.", year_published=2020, pages=200
    )
    created_book = book_service.create_book(db_session, book_in)

    found_book = book_service.get_book_by_id(db_session, created_book.id)
    assert found_book is not None
    assert found_book.title == "Find Me"

    missing_book = book_service.get_book_by_id(db_session, 999)
    assert missing_book is None


def test_get_books_all_and_filter(db_session):
    b1 = schemas.BookCreate(
        title="SciFi Book", author="AAAAA", description="A test description with enough length.", year_published=2020, pages=100,
        genres=[schemas.GenreEnum.SCI_FI]
    )
    b2 = schemas.BookCreate(
        title="Romance Book", author="BBBBB", description="A test description with enough length.", year_published=2020, pages=100,
        genres=[schemas.GenreEnum.ROMANCE]
    )
    book_service.create_book(db_session, b1)
    book_service.create_book(db_session, b2)

    all_books = book_service.get_books(db_session)
    assert len(all_books) == 2

    scifi_books = book_service.get_books(db_session, genre=schemas.GenreEnum.SCI_FI)
    assert len(scifi_books) == 1
    assert scifi_books[0].title == "SciFi Book"


def test_update_book_fields(db_session):
    book_in = schemas.BookCreate(
        title="Old Title", author="Old Author",
        description="A test description with enough length.", year_published=2000, pages=100
    )
    created_book = book_service.create_book(db_session, book_in)

    # Test: Update specific fields using BookUpdate (others default to None)
    update_data = schemas.BookUpdate(title="New Title", author="Old Author",
                                     description="A test description with enough length.", pages=150, year_published=2000)
    updated_book = book_service.update_book(db_session, created_book.id, update_data)

    assert updated_book.title == "New Title"
    assert updated_book.pages == 150
    assert updated_book.author == "Old Author"


def test_update_book_genres_logic(db_session):
    book_in = schemas.BookCreate(
        title="BBB", author="AAAAA", description="A test description with enough length.", year_published=2020, pages=10,
        genres=[schemas.GenreEnum.FICTION]
    )
    created_book = book_service.create_book(db_session, book_in)

    update_none = schemas.BookUpdate(
        title="Updated Title", author="AAAAA", description="A test description with enough length.", year_published=2020,
        pages=10,
        genres=[schemas.GenreEnum.FICTION]
    )
    b_step1 = book_service.update_book(db_session, created_book.id, update_none)
    assert len(b_step1.genres) == 1
    assert b_step1.genres[0].name == "Fiction"

    update_replace = schemas.BookUpdate(
        title="Updated Title", author="AAAAA", description="A test description with enough length.",
        year_published=2020,
        pages=10,
        genres=[schemas.GenreEnum.FANTASY])
    b_step2 = book_service.update_book(db_session, created_book.id, update_replace)
    assert len(b_step2.genres) == 1
    assert b_step2.genres[0].name == "Fantasy"

    update_clear = schemas.BookUpdate(
        title="Updated Title", author="AAAAA", description="A test description with enough length.",
        year_published=2020,
        pages=10,
        genres=[])
    b_step3 = book_service.update_book(db_session, created_book.id, update_clear)
    assert len(b_step3.genres) == 0


def test_delete_book(db_session):
    book_in = schemas.BookCreate(
        title="Delete Me", author="AAAAA", description="A test description with enough length.", year_published=2020, pages=10
    )
    created_book = book_service.create_book(db_session, book_in)

    success = book_service.delete_book(db_session, created_book.id)
    assert success is True

    found = book_service.get_book_by_id(db_session, created_book.id)
    assert found is None

    success_fail = book_service.delete_book(db_session, 999)
    assert success_fail is False


def test_count_books(db_session):
    assert book_service.count_books(db_session) == 0

    book_in = schemas.BookCreate(
        title="BBBBB", author="AAAAAA", description="A test description with enough length.", year_published=2020, pages=10
    )
    book_service.create_book(db_session, book_in)

    assert book_service.count_books(db_session) == 1