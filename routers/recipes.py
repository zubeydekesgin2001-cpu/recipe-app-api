from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
import shutil
import os

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


@router.post("/", response_model=schemas.RecipeResponse)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db)
):
    new_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        category=recipe.category,
        difficulty=recipe.difficulty,
        photo=recipe.photo,
        user_id=recipe.user_id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe


@router.post("/{recipe_id}/upload-image")
async def upload_recipe_image(
    recipe_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    recipe.photo = file_path

    db.commit()
    db.refresh(recipe)

    return {
        "message": "Image uploaded successfully",
        "photo": file_path
    }


@router.get("/", response_model=list[schemas.RecipeResponse])
def get_recipes(
    title: str = None,
    ingredients: str = None,
    category: str = None,
    difficulty: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe)

    if title:
        query = query.filter(models.Recipe.title.contains(title))

    if ingredients:
        query = query.filter(models.Recipe.ingredients.contains(ingredients))

    if category:
        query = query.filter(models.Recipe.category == category)

    if difficulty:
        query = query.filter(models.Recipe.difficulty == difficulty)

    recipes = query.offset(skip).limit(limit).all()

    return recipes


@router.get("/top-rated/")
def top_rated_recipes(db: Session = Depends(get_db)):

    recipes = (
        db.query(
            models.Recipe.title,
            func.avg(models.Rating.value).label("average_rating")
        )
        .join(models.Recipe.ratings)
        .group_by(
            models.Recipe.id,
            models.Recipe.title
        )
        .order_by(func.avg(models.Rating.value).desc())
        .all()
    )

    return [
        {
            "title": recipe.title,
            "average_rating": float(recipe.average_rating)
        }
        for recipe in recipes
    ]

@router.get("/{recipe_id}", response_model=schemas.RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return recipe


@router.put("/{recipe_id}", response_model=schemas.RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db)
):
    existing_recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()

    if not existing_recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    existing_recipe.title = recipe.title
    existing_recipe.description = recipe.description
    existing_recipe.ingredients = recipe.ingredients
    existing_recipe.instructions = recipe.instructions
    existing_recipe.category = recipe.category
    existing_recipe.difficulty = recipe.difficulty
    existing_recipe.photo = recipe.photo
    existing_recipe.user_id = recipe.user_id

    db.commit()
    db.refresh(existing_recipe)

    return existing_recipe


@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    db.delete(recipe)
    db.commit()

    return {"message": "Recipe deleted successfully"}