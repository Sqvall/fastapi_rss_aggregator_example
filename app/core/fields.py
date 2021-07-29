import validators
from tortoise.fields import CharField


class URLField(CharField):

    def __init__(self, **kwargs):
        super().__init__(max_length=65536, min_length=1, **kwargs)

    def to_db_value(self, value: str, instance) -> str:
        if not validators.url(value):
            raise ValueError(f"Value '{value}' is not URL")
        return value
