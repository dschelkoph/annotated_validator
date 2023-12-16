import annotated_types as at

from ..exceptions.annotated_types import (
    AtValidatorError,
    GreaterThanError,
    GreaterThanOrEqualError,
    LessThanError,
    LessThanOrEqualError,
    MultipleOfError,
)


def gt_validator(metadata: at.Gt, value) -> list[AtValidatorError]:
    if metadata.gt >= value:
        return [GreaterThanError(metadata.gt, value)]
    return []


def ge_validator(metadata: at.Ge, value) -> list[AtValidatorError]:
    if metadata.ge > value:
        return [GreaterThanOrEqualError(metadata.ge, value)]
    return []


def lt_validator(metadata: at.Lt, value) -> list[AtValidatorError]:
    if metadata.lt <= value:
        return [LessThanError(metadata.lt, value)]
    return []


def le_validator(metadata: at.Le, value) -> list[AtValidatorError]:
    if metadata.le < value:
        return [LessThanOrEqualError(metadata.le, value)]
    return []


def multiple_of_validator(metadata: at.MultipleOf, value) -> list[AtValidatorError]:
    if value % metadata.multiple_of != 0:
        return [MultipleOfError(metadata.multiple_of, value)]
    return []
