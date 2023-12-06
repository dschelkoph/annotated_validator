"""Errors from the `number_validators` module."""

from .validator import ValidatorError


class LowBoundError(ValidatorError):
    """Error when a number is smaller than the lower bound."""

    def __init__(self, bound: int, value: int):
        self.bound = bound
        self.value = value
        self.message = f"{value} is smaller than the lower bound: {bound}"
        super().__init__(self.message)


class HighBoundError(ValidatorError):
    """Error when a number is larger than the higher bound."""

    def __init__(self, bound: int, value: int):
        self.bound = bound
        self.value = value
        self.message = f"{value} is larger than the higher bound: {bound}"
        super().__init__(self.message)
