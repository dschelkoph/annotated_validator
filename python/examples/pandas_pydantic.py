"""Show a Pydantic Model validating using the same metadata used for validating dataclasses and functions."""

import logging
from typing import Annotated, Self, TypeAlias

import pandas as pd
from pydantic import BaseModel, model_validator
from rich.logging import RichHandler

from annotated_validator.pandas_validators import RequiredColumns
from annotated_validator.validator import class_annotated_validator

logger = logging.getLogger(__name__)


DfWithItemColumns: TypeAlias = Annotated[
    pd.DataFrame,
    RequiredColumns(
        {
            "name": "object",
            "cost": "int64",
            "quantity": "int64",
            "on_sale": "bool",
        }
    ),
]
"""Dataframe with columns that represent an item."""


class Item(BaseModel):
    """An item in a store.

    Used for inventory.
    """

    name: str
    cost: int
    quantity: int
    on_sale: bool


class PydanticLocations(BaseModel):
    """Keep track of inventories from multiple locations."""

    cleveland: DfWithItemColumns
    columbus: DfWithItemColumns
    cincinnati: DfWithItemColumns

    class Config:
        arbitrary_types_allowed = True

    @model_validator(mode="after")
    def model_validate_annotated(self) -> Self:
        return class_annotated_validator(self)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
    )
    cleveland_df = pd.DataFrame(
        [
            Item(name="Pens", cost=75, quantity=80, on_sale=False).model_dump(),
            Item(name="Notepad", cost=300, quantity=40, on_sale=True).model_dump(),
        ]
    )
    columbus_df = pd.DataFrame(
        {"name": ["Scissors", "Highlighter"], "cost": [1000, 150], "quantity": [35.4, 54]}
    )

    cincinnati_df = pd.DataFrame(
        [
            Item(name="Paperclips", cost=250, quantity=600, on_sale=False).model_dump(),
            Item(name="Eraser", cost=50, quantity=47, on_sale=True).model_dump(),
        ]
    )

    # this will thow an error because of mismatched data in the columbus_df
    total_inventory = PydanticLocations(
        cleveland=cleveland_df, columbus=columbus_df, cincinnati=cincinnati_df
    )


if __name__ == "__main__":
    main()
