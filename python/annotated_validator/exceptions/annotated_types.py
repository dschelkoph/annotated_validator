import annotated_types as at

from .validator import ValidatorError


class AtValidatorError(ValidatorError):
    ...


class InvalidMetadataError(AtValidatorError):
    def __init__(self, metadata: at.BaseMetadata, message: str):
        self.metadata = metadata
        self.message = message
        super().__init__(self.message)


class NotSupportedAnnotatedTypeError(AtValidatorError):
    def __init__(self, metadata: at.BaseMetadata):
        self.metadata = metadata
        self.message = f"{metadata} is not a supported type for validation."
        super().__init__(self.message)


class GreaterThanError(AtValidatorError):
    def __init__(self, bound, value):
        self.bound = bound
        self.value = value
        self.message = f"Value: {value} is not greater than the Bound: {bound}"
        super().__init__(self.message)


class GreaterThanOrEqualError(AtValidatorError):
    def __init__(self, bound, value):
        self.bound = bound
        self.value = value
        self.message = f"Value: {value} is not greater than or equal to the Bound: {bound}"
        super().__init__(self.message)


class LessThanError(AtValidatorError):
    def __init__(self, bound, value):
        self.bound = bound
        self.value = value
        self.message = f"Value: {value} is not less than the Bound: {bound}"
        super().__init__(self.message)


class LessThanOrEqualError(AtValidatorError):
    def __init__(self, bound, value):
        self.bound = bound
        self.value = value
        self.message = f"Value: {value} is not less than or equal to the Bound: {bound}"
        super().__init__(self.message)


class MultipleOfError(AtValidatorError):
    def __init__(self, multiple, value):
        self.multiple = multiple
        self.value = value
        self.message = f"Value: {value} is not a multiple of {multiple}"
        super().__init__(self.message)


class MinLenError(AtValidatorError):
    def __init__(self, min_len: int, value):
        self.min_len = min_len
        self.value = value
        self.message = (
            f"Length of `{value}` ({len(value)}) is less than the minimum length: {min_len}."
        )
        super().__init__(self.message)
