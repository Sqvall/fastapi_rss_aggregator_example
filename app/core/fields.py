import validators
from tortoise.exceptions import FieldError
from tortoise.fields import CharField


class URLField(CharField):

    def __init__(self, **kwargs):
        super().__init__(max_length=65536, min_length=1, **kwargs)

    def to_db_value(self, value: str, instance) -> str:
        if not validators.url(value):
            raise FieldError(f"Value '{value}' is invalid URL value")
        return value
