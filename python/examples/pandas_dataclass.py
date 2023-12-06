"""Show a dataclass inheriting from `ValidateAnnotated` to validate a Pandas Dataframe."""

import logging
from dataclasses import dataclass
from typing import Annotated, TypeAlias

import pandas as pd
from pydantic import BaseModel
from rich.logging import RichHandler

from annotated_validator.pandas_validators import RequiredColumns
from annotated_validator.validator import (
    ValidateAnnotated,
)

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


@dataclass
class Locations(ValidateAnnotated):
    """Keep track of inventories from multiple locations."""

    cleveland: DfWithItemColumns
    columbus: DfWithItemColumns
    cincinnati: DfWithItemColumns


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
    total_inventory = Locations(cleveland_df, columbus_df, cincinnati_df)


if __name__ == "__main__":
    main()
