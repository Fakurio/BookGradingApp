from .. import models, schemas
from sqlalchemy.orm import Session

def create_review(db: Session, review: schemas.ReviewCreate, book_id: int):
    """
    Dodaje recenzję do książki
    """
    db_review = models.ReviewDB(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def count_reviews(db: Session) -> int:
    """
    Zwraca liczbę wszystkich recenzji w systemie
    """
    return db.query(models.ReviewDB).count()