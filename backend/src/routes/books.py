from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import schemas
from ..services import book_service
from ..database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    db: Session = Depends(get_db),
    genre: Optional[schemas.GenreEnum] = Query(None, description="Filter books by genre")
):
    """
    Endpoint do pobrania wszystkich książek z opcjonalnym filtrowaniem po gatunkach
    :param db: sesja bazy danych
    :param genre: gatunek z query string ?genre=
    """
    return book_service.get_books(db, genre)

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book_by_id(
    book_id: int,
    db: Session = Depends(get_db),
):
    """
    Endpoint do pobrania książki po jej ID
    """
    return book_service.get_book_by_id(db, book_id)


@router.post("/", response_model=schemas.BookResponse)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint do dodania nowej książki
    """
    return book_service.create_book(db, book)

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
        book_id: int,
        book: schemas.BookUpdate,
        db: Session = Depends(get_db)
):
    """
    Endpoint do aktualizacji książki po ID
    """
    db_book = book_service.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book_service.update_book(db, book_id, book)

@router.delete("/{book_id}")
def delete_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    """
    Endpoint do usuwania książki po ID
    """
    success = book_service.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"status": "success", "message": "Book deleted"}



