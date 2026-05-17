import re

from pydantic import BaseModel, Field, field_validator


class User(BaseModel):

    name: str
    id: int


class UserAge(BaseModel):

    name: str
    age: int



class Feedback(BaseModel):

    name: str
    message: str



FORBIDDEN_WORDS = ["кринж", "рофл", "вайб"]


class FeedbackValidated(BaseModel):


    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def message_must_be_clean(cls, value: str) -> str:
        lowered = value.lower()
        for word in FORBIDDEN_WORDS:
            # \w* позволяет поймать слово в любом падеже: "кринжа", "кринжом" и т.д.
            pattern = re.compile(word + r"\w*", re.IGNORECASE)
            if pattern.search(lowered):
                raise ValueError("Использование недопустимых слов")
        return value
