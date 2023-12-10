from typing import Protocol

import annotated_types as at

from ..exceptions.annotated_types import NotSupportedAnnotatedTypeError
from ..exceptions.validator import ValidatorError
from .comparison import ge_validator, gt_validator, le_validator, lt_validator


class BaseValidator(Protocol):
    def __call__(self, metadata: at.BaseMetadata, value) -> list[ValidatorError]:
        ...


SUPPORTED_ANNOTATED_TYPES: dict[at.BaseMetadata, BaseValidator] = {
    at.Ge: ge_validator,
    at.Gt: gt_validator,
    at.Le: le_validator,
    at.Lt: lt_validator,
}


def get_at_validators(metadata: at.BaseMetadata) -> list[BaseValidator]:
    metadata_iter = [metadata] if not isinstance(metadata, at.GroupedMetadata) else metadata

    exceptions = []
    validators = []
    for sub_metadata in metadata_iter:
        if (sub_metadata_type := type(sub_metadata)) not in SUPPORTED_ANNOTATED_TYPES:
            exceptions.append(NotSupportedAnnotatedTypeError(sub_metadata_type))
            continue
        validators.append(SUPPORTED_ANNOTATED_TYPES[sub_metadata_type])
    if exceptions:
        raise ExceptionGroup(
            f"Errors finding validators for `GroupedMetadata`: {metadata}", exceptions
        )
    print(validators)
    return validators
