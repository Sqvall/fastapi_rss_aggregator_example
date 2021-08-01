from pydantic import BaseModel, BaseConfig


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class CamelModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        alias_generator = convert_field_to_camel_case
