import logging
from typing import NamedTuple, Protocol

import annotated_types as at

from ..exceptions.annotated_types import AtValidatorError
from .length_comparison import min_len_validator
from .numerical_comparison import (
    ge_validator,
    gt_validator,
    le_validator,
    lt_validator,
    multiple_of_validator,
)

logger = logging.getLogger(__name__)


class BaseValidator(Protocol):
    def __call__(self, metadata: at.BaseMetadata, value) -> list[AtValidatorError]:
        ...


def unsuported_validator(metadata: at.BaseMetadata, value) -> list[AtValidatorError]:
    logger.debug("%s (Value: %s) doesn't have an implemented validator.")
    return []


SUPPORTED_ANNOTATED_TYPES: dict[at.BaseMetadata, BaseValidator] = {
    at.Ge: ge_validator,
    at.Gt: gt_validator,
    at.Le: le_validator,
    at.Lt: lt_validator,
    at.MultipleOf: multiple_of_validator,
    at.MinLen: min_len_validator,
}


class UnpackedBaseMetadata(NamedTuple):
    py_type: at.BaseMetadata
    validator: BaseValidator


def get_at_validators(metadata: at.BaseMetadata) -> list[UnpackedBaseMetadata]:
    metadata_iter = [metadata] if not isinstance(metadata, at.GroupedMetadata) else metadata

    unpacked_metadata = []
    for sub_metadata in metadata_iter:
        validator = SUPPORTED_ANNOTATED_TYPES.get(type(sub_metadata), unsuported_validator)
        unpacked_metadata.append(UnpackedBaseMetadata(py_type=sub_metadata, validator=validator))
    return unpacked_metadata
