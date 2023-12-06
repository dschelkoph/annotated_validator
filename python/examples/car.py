import logging
from dataclasses import dataclass
from typing import Annotated

from rich.logging import RichHandler

from annotated_validator.number_validators import NumberRange
from annotated_validator.validator import ValidateAnnotated

logger = logging.getLogger(__name__)


@dataclass
class Car(ValidateAnnotated):
    make: str
    model: str
    doors: Annotated[int | float, NumberRange(low=1, high=8)]


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
    )
    valid_car = Car("Toyta", "Camry", doors=2)
    invalid_car = Car("Honda", "Accord", doors=9)


if __name__ == "__main__":
    main()