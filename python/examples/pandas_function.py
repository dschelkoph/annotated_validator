import logging
from typing import Annotated, Any, TypeAlias

import pandas as pd
from rich.logging import RichHandler

from annotated_validator.pandas_validators import RequiredColumns
from annotated_validator.validator import (
    validate_annotated,
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


@validate_annotated
def get_sale_items(df: DfWithItemColumns) -> DfWithItemColumns:
    return df.loc[df["on_sale"] == True]


@validate_annotated
def add_items_by_dict(df: DfWithItemColumns, items: dict[str, list[Any]]) -> DfWithItemColumns:
    return pd.concat([df, pd.DataFrame(items)])


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
    )

    columbus_df = pd.DataFrame(
        {"name": ["Scissors", "Highlighter"], "cost": [1000, 150], "quantity": [35, 54]}
    )
    # columbus_sale_df = get_sale_items(columbus_df)

    # if you comment the line above, `add_items_by_dict` thows an error on the return value
    cleveland_df = pd.DataFrame(
        {
            "name": ["Pens", "Notepad"],
            "cost": [75, 300],
            "quantity": [80, 40],
            "on_sale": [True, False],
        }
    )
    cleveland_df = add_items_by_dict(
        cleveland_df, {"name": ["Chair"], "cost": [20000], "quantity": [20.4]}
    )


if __name__ == "__main__":
    main()
