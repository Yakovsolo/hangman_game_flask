from pydantic import BaseModel, validator
from typing import List


class WordCreate(BaseModel):
    word: str
    word_length: int
    category: str
    times_called: int
    times_answered: int
    times_lost: int

    class Config:
        json_schema_extra = {
            "example": {
                "word": "orange",
                "word_length": 6,
                "category": "food",
                "times_called": 0,
                "times_answered": 0,
                "times_lost": 0,
            }
        }

    @validator("category")
    def validate_category(cls, value):
        allowed_categories = [
            "animals",
            "home",
            "jobs",
            "food",
            "clothes",
            "countries",
            "cities",
            "space",
            "mountains",
        ]
        if value not in allowed_categories:
            raise ValueError("Invalid category")
        return value


class WordResponse(BaseModel):
    id: int
    word: str
    word_length: int
    category: str
    times_called: int
    times_answered: int
    times_lost: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "word": "orange",
                "word_length": 6,
                "category": "food",
                "times_called": 0,
                "times_answered": 0,
                "times_lost": 0,
            }
        }


class WordUpdate(BaseModel):
    id: int
    word: str
    word_length: int
    category: str
    times_called: int
    times_answered: int
    times_lost: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "word": "orange",
                "word_length": 6,
                "category": "food",
                "times_called": 1,
                "times_answered": 0,
                "times_lost": 1,
            }
        }
