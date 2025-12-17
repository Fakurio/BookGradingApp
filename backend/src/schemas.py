from datetime import date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class GenreEnum(str, Enum):
    """
    Enum z dozwolonymi wartościami dla gatunków książek
    """
    FICTION = "Fiction"
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    MYSTERY = "Mystery"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    ROMANCE = "Romance"

class ReviewCreate(BaseModel):
    """
    Klasa DTO do tworzenia recenzji
    """
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Comment must be between 5 and 500 characters"
    )

class ReviewResponse(ReviewCreate):
    """
    Klasa DTO do zwracania recenzji
    """
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    """
    Klasa DTO dla dodawania ksiązki
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Title cannot be empty and max 150 characters"
    )
    author: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Author cannot be empty and max 100 characters"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Description must be at least 10 characters"
    )
    year_published: int = Field(..., ge=1800, le=date.today().year,
                                description="Year must be between 1800 and today's year")
    pages: int = Field(..., ge=0, description="Number of pages must be greater than 0")
    genres: List[GenreEnum] = []

class BookUpdate(BookCreate):
    """
    Klasa DTO dla aktualizacji książki
    """
    genres: Optional[List[GenreEnum]] = None

class GenreResponse(BaseModel):
    """
    Klasa DTO do zwracania gatunku
    """
    name: GenreEnum
    model_config = ConfigDict(from_attributes=True)

class BookResponse(BookCreate):
    """
    Klasa DTO do zwracania książki
    """
    id: int
    reviews: List[ReviewResponse] = []
    genres: List[GenreResponse] = []
    model_config = ConfigDict(from_attributes=True)

