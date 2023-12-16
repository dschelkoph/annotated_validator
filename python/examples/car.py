import logging
from dataclasses import dataclass, field
from typing import Annotated, Any

import annotated_types as at
from pydantic import AfterValidator, TypeAdapter
from pydantic_core import core_schema
from rich.logging import RichHandler

from annotated_validator.validator import ValidateAnnotated

logger = logging.getLogger(__name__)


@dataclass
class Car(ValidateAnnotated):
    make: str
    model: Annotated[str, at.MinLen(3)]
    doors: Annotated[int | float, at.Interval(ge=1, le=8)]


class GreaterThanValidationError(ValueError):
    def __init__(self, bound: int):
        self.bound = bound
        self.message = f"Must be greater than {bound}."
        super().__init__(self.message)


@dataclass(frozen=True)
class AfterValidatorWrapper(AfterValidator):
    func: core_schema.NoInfoValidatorFunction | core_schema.WithInfoValidatorFunction = field(
        init=False
    )

    def validate(self, value: Any) -> Any:
        raise NotImplementedError()

    def __post_init__(self):
        super().__init__(self.validate)


@dataclass(frozen=True)
class GreaterThan(AfterValidatorWrapper):
    bound: int

    def validate(self, value: int) -> int:
        if value <= self.bound:
            raise GreaterThanValidationError(self.bound)
        return value


def greater_than_zero(value: int) -> int:
    if value <= 0:
        raise ValueError("Must be greater than 0.")
    return value


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
    )
    # valid_car = Car("Toyta", "Ca", doors=9)
    # invalid_car = Car("Honda", "Accord", doors=9)

    PositiveIntAdapter = TypeAdapter(Annotated[int, GreaterThan(2)])
    PositiveIntAdapter.validate_python(-1)


if __name__ == "__main__":
    main()
