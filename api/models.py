import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")

class TunedModel(BaseModel):
    class Config:
        orm_mode = True

class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @validator("name")
    def name_validator(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contain only letters"
            )
        return value

    @validator("surname")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contain only letters"
            )
        return value