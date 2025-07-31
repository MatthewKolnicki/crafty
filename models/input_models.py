from pydantic import BaseModel


class QuestionOneInput(BaseModel):
    Type: list[str]


class QuestionTwoInput(BaseModel):
    dictionary: dict
    delimiter: str = "."
    parent_key: str = ""
