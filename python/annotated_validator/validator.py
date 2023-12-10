"""Base functionality required to perform validation on Classes and Functions."""

import functools
import inspect
import logging
from abc import abstractmethod
from typing import Any, NamedTuple, TypeAlias, get_type_hints

from annotated_types import BaseMetadata, GroupedMetadata

from .annotated_types_validators import get_at_validators
from .exceptions.validator import ValidatorError

logger = logging.getLogger(__name__)


class BaseMetaValidator(BaseMetadata):
    """Base Class for all Validation Classes.

    Metadata is checked to see if it of type `Validator` in order to be used for validation.
    """

    @staticmethod
    def at_validate(metadata: "BaseMetaValidator", value) -> None | ExceptionGroup[ValidatorError]:
        return metadata.validate(value)

    @abstractmethod
    def validate(self, value) -> None | ExceptionGroup[ValidatorError]:
        ...


class ParamData(NamedTuple):
    """Tuple that contains both the value and type of a parameter."""

    value: Any
    """Assigned value of a parameter."""
    py_type: type
    """Type annotation of a parameter."""


ValidatorExceptionGroup: TypeAlias = ExceptionGroup[ValidatorError]
"""All exceptions from a single validator are contained into this exeception group."""

ParameterExceptionGroup: TypeAlias = ExceptionGroup[ValidatorExceptionGroup]
"""All exceptions for a parameter (can include errors from multiple validators) are contained in this exception group."""


def annotated_validator(parameters: dict[str, ParamData]) -> list[ParameterExceptionGroup]:
    """Review all passed in parameters and perform validation if the proper metatdata is found.

    Metadata must be of type `Validator` to be used for validation.
    """
    parameter_exeception_groups = []

    for param_name, param_data in parameters.items():
        param_metadata = getattr(param_data.py_type, "__metadata__", None)
        if not param_metadata:
            logger.debug("%s doesn't contain metadata, skipping validation.", param_name)
            continue
        validation_exception_groups = []
        for metadata in param_metadata:
            if not isinstance(metadata, BaseMetaValidator | BaseMetadata | GroupedMetadata):
                logger.debug(
                    "Metadata: %s was not an instance of the `Validator` or `annotated_types.BaseMetadata`.",
                    metadata,
                )
                continue
            # this is metadata from `annotated_types` and should be validated
            if isinstance(metadata, BaseMetaValidator):
                if errors := metadata.validate(param_data.value):
                    validation_exception_groups.append(errors)
            elif isinstance(metadata, BaseMetadata | GroupedMetadata):
                at_validators = get_at_validators(metadata)
                errors = []
                for at_validator in at_validators:
                    at_validator_result = at_validator(metadata, param_data.value)
                    errors.extend(at_validator_result)
                if errors:
                    validation_exception_groups.append(
                        ExceptionGroup(f"`{metadata.__class__.__name__}` Validation Errors", errors)
                    )
        if validation_exception_groups:
            parameter_exeception_groups.append(
                ExceptionGroup(f"`{param_name}` Validation Errors", validation_exception_groups)
            )
            validation_exception_groups = []
    return parameter_exeception_groups


def class_annotated_validator(obj: Any) -> Any:
    """Used to validate a Class.

    Can be used to validate a Pydantic Model if you include the following method in the Pydantic Model:

    ```
    @model_validator(mode="after")
    def model_validate_annotated(self) -> Self:
        return class_annotated_validator(self)
    ```

    Gathers info from the class that can be used in `annotated_validator`.
    """
    param_map = {
        param_name: ParamData(value=getattr(obj, param_name), py_type=param_type)
        for param_name, param_type in get_type_hints(obj, include_extras=True).items()
        if param_type.__name__ == "Annotated"
    }
    errors = annotated_validator(param_map)
    if errors:
        raise ExceptionGroup(f"`{obj.__class__.__name__}` Validation Errors", errors)  # noqa: TRY003
    return obj


class ValidateAnnotated:
    """If inherited by a dataclass, perform validation on parameters with the proper metadata."""

    def __post_init__(self):
        class_annotated_validator(self)


def validate_annotated(func):
    """Decorator for functions that performs validation on parameters with the proper metadata.

    Also validates the return value if properly annotated.
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        # get introspection data on function
        func_locals = locals()
        func_signature = inspect.signature(wrapped_func)

        # get map of parameter names to values
        bound_args = func_signature.bind(*func_locals["args"], **func_locals["kwargs"])
        bound_args.apply_defaults()
        value_map = bound_args.arguments

        type_hints = {
            param_name: param_sig.annotation
            for param_name, param_sig in func_signature.parameters.items()
            if param_sig.annotation.__name__ == "Annotated"
        }

        param_map = {
            param_name: ParamData(value=value_map[param_name], py_type=py_type)
            for param_name, py_type in type_hints.items()
        }
        logger.debug("Checked Inputs: %s", param_map)
        errors = annotated_validator(param_map)
        if errors:
            raise ExceptionGroup(  # noqa: TRY003
                f"Validation error(s) when processing inputs for `{func.__name__}`. Checked Inputs: {param_map}",
                errors,
            )

        return_value = func(*args, **kwargs)

        if (return_type := func_signature.return_annotation) != inspect.Parameter.empty:
            return_param_map = {"return": ParamData(return_value, return_type)}
            logger.debug("Checked Return: %s", return_param_map)
            errors = annotated_validator(return_param_map)
            if errors:
                raise ExceptionGroup(  # noqa: TRY003
                    f"Validation error on return value for `{func.__name__}`. Checked Return: {return_param_map}.",
                    errors,
                )
        return return_value

    return wrapped_func
