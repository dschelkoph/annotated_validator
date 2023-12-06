import pytest
from pydantic import BaseModel, ValidationError


class People(BaseModel):
    people: dict[str, int]


def test_pydantic_validation():
    people_class = People(people={"john": 1, "jane": 2})
    people_class = People(people={"john": "1", "jane": "2"})


def test_pydantic_validation_failure():
    with pytest.raises(ValidationError):
        people_class = People(people=(("john", 1), ("jane", 2)))
    with pytest.raises(ValidationError):
        people_class = People(people={"john": 1, "jane": "two"})
