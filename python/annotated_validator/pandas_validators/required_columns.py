"""Validates that a Pandas Dataframe has the required columns with the correct types."""

from dataclasses import dataclass

import pandas as pd

from ..exceptions.pandas import RequiredColumnDoesntExistError, RequiredColumnTypeMismatchError
from ..exceptions.validator import ValidatorError
from ..validator import BaseMetaValidator


@dataclass
class RequiredColumns(BaseMetaValidator):
    """Validates that a Pandas Dataframe has the required columns with the correct types."""

    column_map: dict[str, str]
    """Keys are column names, values are Pandas Datafram Types."""

    def validate(self, value: pd.DataFrame) -> None | ExceptionGroup[ValidatorError]:
        exceptions = []
        column_index = value.columns
        value_column_map = {column_name: value[column_name].dtype for column_name in column_index}
        for column_name, required_dtype in self.column_map.items():
            if column_name not in value_column_map:
                exceptions.append(RequiredColumnDoesntExistError(column_name))
                continue
            if required_dtype != "object" and required_dtype != (
                current_dtype := value_column_map[column_name]
            ):
                exceptions.append(
                    RequiredColumnTypeMismatchError(column_name, required_dtype, current_dtype)
                )
        return ExceptionGroup("pandas_required_columns", exceptions) if exceptions else None
