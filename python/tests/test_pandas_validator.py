from dataclasses import dataclass
from typing import Annotated, Any, TypeAlias

import pandas as pd

from annotated_validator.required_columns import RequiredColumns
from annotated_validator.validator import validate_annotated

DfWithItemColumns: TypeAlias = Annotated[
    pd.DataFrame,
    RequiredColumns(
        {
            "name": "object",
            "cost": "int64",
            "quantity": "int64",
            "taxable": "bool",
        }
    ),
]
"""Dataframe with at least the following columns: name, cost, quantity and taxable."""


@dataclass
class Item:
    name: str
    cost: int
    quantity: int
    taxable: bool


def add_item(
    df: DfWithItemColumns, item: dict[str, list[Any]], *args, **kwargs
) -> DfWithItemColumns:
    return pd.concat([df, pd.DataFrame.from_dict(item)])


def test_required_columns_validator():
    df = pd.DataFrame([Item("Pens", 75, 80, True), Item("Notepad", 300, 40, True)])
    validate_annotated(add_item)(
        df,
        {"name": ["Printer"], "cost": [10000], "quantity": [20], "taxable": [True]},
        "test",
        test="test_kwargs",
    )


if __name__ == "__main__":
    test_required_columns_validator()
