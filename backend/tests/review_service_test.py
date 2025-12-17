import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.services import review_service, book_service
from src import schemas

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_review(db_session):
    book_in = schemas.BookCreate(
        title="Book for Review", author="AAAA", description="A test description with enough length.", year_published=2020, pages=10
    )
    book = book_service.create_book(db_session, book_in)

    review_in = schemas.ReviewCreate(rating=5, comment="Great book!")
    review = review_service.create_review(db_session, review_in, book.id)

    assert review.id is not None
    assert review.rating == 5
    assert review.book_id == book.id

    db_session.refresh(book)
    assert len(book.reviews) == 1
    assert book.reviews[0].comment == "Great book!"


def test_count_reviews(db_session):
    book_in = schemas.BookCreate(
        title="BBBB", author="AAAAA", description="A test description with enough length.", year_published=2020, pages=10
    )
    book = book_service.create_book(db_session, book_in)

    assert review_service.count_reviews(db_session) == 0

    review_in = schemas.ReviewCreate(rating=4, comment="Good ..........")
    review_service.create_review(db_session, review_in, book.id)

    assert review_service.count_reviews(db_session) == 1