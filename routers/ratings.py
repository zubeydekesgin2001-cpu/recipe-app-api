from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)

@router.post("/", response_model=schemas.RatingResponse)
def create_rating(
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db)
):
    new_rating = models.Rating(
        value=rating.value,
        comment=rating.comment,
        user_id=rating.user_id,
        recipe_id=rating.recipe_id
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating


@router.get("/", response_model=list[schemas.RatingResponse])
def get_ratings(db: Session = Depends(get_db)):
    ratings = db.query(models.Rating).all()
    return ratings