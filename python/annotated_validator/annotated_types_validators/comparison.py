import annotated_types as at

from ..exceptions.annotated_types import (
    GreaterThanError,
    GreaterThanOrEqualError,
    LessThanError,
    LessThanOrEqualError,
)
from ..exceptions.validator import ValidatorError


def gt_validator(metadata: at.Gt, value) -> list[ValidatorError]:
    if metadata.gt >= value:
        return [GreaterThanError(metadata.gt, value)]
    return []


def ge_validator(metadata: at.Ge, value) -> list[ValidatorError]:
    if metadata.ge > value:
        return [GreaterThanOrEqualError(metadata.ge, value)]
    return []


def lt_validator(metadata: at.Lt, value) -> list[ValidatorError]:
    if metadata.lt <= value:
        return [LessThanError(metadata.lt, value)]
    return []


def le_validator(metadata: at.Le, value) -> list[ValidatorError]:
    if metadata.le < value:
        return [LessThanOrEqualError(metadata.le, value)]
    return []
