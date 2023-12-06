"""Base Exception for all Validator Errors."""


class ValidatorError(Exception):
    """Base Exception for all Validator Errors.

    Errors that inherit from this Exception are collected in an Exception Group during validation.
    """

    ...
