from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..services import review_service, book_service
from ..database import get_db

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/{book_id}", response_model=schemas.ReviewResponse)
def rate_book(
    book_id: int,
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint do dodania recenzji dla książki po jej ID
    """
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return review_service.create_review(db, review, book_id)