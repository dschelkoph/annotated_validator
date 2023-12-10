import annotated_types as at

from .validator import ValidatorError


class AtValidatorError(ValidatorError):
    ...


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
