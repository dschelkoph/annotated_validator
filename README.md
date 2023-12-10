# annotated_validator
Use Python typing metadata to validate parameters in classes and functions. Working on compatability with `annotated_types`, a collection of Annotated Types used in Pydantic.

# Create a Validator
Create a concrete class from the base class: `annotated_validator.validator.Validator`.

# Use a Validator
> For validation to work, validation metadata must be of type `annotated_validator.validator.Validator`, `annotated_types.BaseMetadata` or `annotated_types.GroupedMetadata`!

The following are the only supported `annotated_types.BaseMetadata` types:
- Ge
- Gt
- Le
- Lt

## Function
1. Annotate your input parameters and return value with the `Annotated` type and metadata that is of type `Validator`, `annotated_types.BaseMetadata` or `annotated_types.GroupedMetadata`.
1. Use the `annotated_validator.validator.validate_annotated` decorator

```python
from typing import Annotated, TypeAlias

# Can use from certain types from `annotated_types`
from annotated_types import Gt
# NumberRange inherits from `Validator`
from annotated_validator.number_validators import NumberRange
from annotated_validator.validator import validate_annotated

# Using TypeAliases allows you to re-use the validation logic wherever needed.
# Gt and NumberRange are performing the same function and can both be validated
PositiveInt: TypeAlias = Annotated[int, NumberRange(low=0, high=None)]
AtPositiveInt: TypeAlias = Annotated[int, Gt(0)]

@validate_annotated
def add_positive_integers(num_1: PositiveInt, num_2: AtPositiveInt,  num_3: int) -> PositiveInt:
    # `num_1` and the return will be validated using `NumberRange`
    # Since num_2 insn't annotated with metadata, it is not validated
    return num_1 + num_2

# Will throw an error on `num_1` and `num_2` since they are both negative
add_positive_integers(-1, -1, 2)
# Will throw an error since the return is negative
add_positive_integers(1, 1, -3)
```

## Dataclass
Inherit from `annotated_validator.validator.ValidateAnnotated` and parameters with the correct metadata will be validated on creation:

```python
from dataclasses import dataclass

from annotated_validator.validator import ValidateAnnotated

# num_1 will be validated on creation, num_2 will not
@dataclass
class Numbers(ValidateAnnotated):
    num_1: PositiveInt
    num_2: int

# error will be thrown because num_1 is not positive
Numbers(-1, 1)
# no error is thrown
Numbers(1, -1)
```

## Pydantic Model
Use a model validator to use additional validation metadata in addtion to what Pydantic offers:

```python
from typing import Self, Annotated

from pydantic import BaseModel, model_validator, Field

class Numbers(BaseModel):
    num_1: PositiveInt
    num_2: Annotated[int, Field(gt=0)]

    @model_validator(mode="after")
    def model_validate_annotated(self) -> Self:
        return class_annotated_validator(self)

# error will be thrown because num_1 is not positive
Numbers(-1, 1)
# error is thrown since pydantic is validating `num_2`
Numbers(1, -1)
```