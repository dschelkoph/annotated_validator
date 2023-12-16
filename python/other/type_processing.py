from __future__ import annotations

from dataclasses import dataclass
from typing import Union, get_args, get_origin


def get_comparable_type(py_type: type) -> type:
    origin = get_origin(py_type)
    if not origin:
        return py_type
    if origin.__name__ not in {"Union", "UnionType", "Annotated"}:
        return origin
    arguments = get_args(py_type)
    if origin.__name__ == "Annotated":
        return get_comparable_type(arguments[0])
    if origin.__name__ in {"Union", "UnionType"}:
        types_without_arguments = tuple(get_comparable_type(type_arg) for type_arg in arguments)
        return Union[*types_without_arguments]
    raise ValueError()


class TypeData:
    origin: type
    arguments: tuple
    metadata: tuple
    valid_types: type

def get_type_data(py_type: type) -> dict[type, TypeData]:
    origin = get_origin(py_type)
    if not origin:
        return {py_type: TypeData(arguments=(), metadata=())}
    if origin.__name__ not in {"Union", "UnionType", "Annotated"}:
        return {py_type: TypeData(arguments=get_args(py_type), metadata=())}
    if origin.__name__ in "Annotated":



@dataclass(slots=True)
class TypeAnnotation:
    origin: type
    arguments: tuple
    metadata: tuple
    valid_base_type: type

    @classmethod
    def from_py_type(cls, py_type: type) -> TypeAnnotation:
        origin = get_origin(py_type)
        # a simple type, with no arguments, set origin to original type
        if not origin:
            origin = py_type
            valid_type = py_type

        arguments = get_args(py_type)
        metadata = ()
        if origin.__name__ == "Annotated":
            metadata = arguments[1:]
            arguments = (arguments[0],)

        valid_type = get_comparable_type(py_type)

        type_annotation = TypeAnnotation(origin, arguments, metadata, valid_type)
        print(type_annotation)
        return type_annotation
