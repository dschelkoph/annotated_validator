import annotated_types as at

from ..exceptions.annotated_types import AtValidatorError, InvalidMetadataError, MinLenError


def min_len_validator(metadata: at.MinLen, value) -> list[AtValidatorError]:
    if metadata.min_length < 0:
        return [
            InvalidMetadataError(
                metadata,
                message=f"`min_length`: {metadata.min_length} must be greater than or equal to 0.",
            )
        ]
    if metadata.min_length > len(value):
        return [MinLenError(metadata.min_length, value)]
    return []
