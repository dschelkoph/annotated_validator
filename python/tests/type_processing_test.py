from typing import Annotated, Optional, TypeAlias, Union, get_args, get_origin

import pytest

from talk.type_processing import TypeAnnotation

TestInteger: TypeAlias = Annotated[int, "test_integer"]
"""integer with metadata."""


@pytest.mark.parametrize("py_type", [int, float, str, bytes, bytearray, list, set, dict])
def test_basic_types(py_type: type):
    type_annotation = TypeAnnotation.from_py_type(py_type)
    assert type_annotation.origin == py_type
    assert type_annotation.arguments == ()
    assert type_annotation.metadata == ()
    assert type_annotation.valid_base_type == py_type


# TODO: Does `Optional` get converted to `UnionType` in every Python Version?
@pytest.mark.parametrize(
    "py_type",
    [
        int | float,
        Union[float, int],
        int | None,
        Optional[int],
    ],
)
def test_basic_types_with_union(py_type: type):
    type_annotation = TypeAnnotation.from_py_type(py_type)
    assert type_annotation.origin == get_origin(py_type)
    arguments = get_args(py_type)
    assert type_annotation.arguments == arguments
    assert type_annotation.metadata == ()
    assert type_annotation.valid_base_type == py_type


@pytest.mark.parametrize(
    "py_type,valid_type",
    [
        (Union[int, Union[str, float]], Union[int, str, float]),
        (int | str | Union[float, bytes], Union[int, str, float, bytes]),
    ],
)
def test_basic_types_with_nested_union(py_type: type, valid_type: type):
    type_annotation = TypeAnnotation.from_py_type(py_type)
    assert type_annotation.origin == get_origin(py_type)
    arguments = get_args(py_type)
    assert type_annotation.arguments == arguments
    assert type_annotation.metadata == ()
    assert type_annotation.valid_base_type == valid_type


@pytest.mark.parametrize("py_type", [Annotated[int, "integer"]])
def test_basic_types_with_annotated(py_type: type):
    type_annotation = TypeAnnotation.from_py_type(py_type)
    assert type_annotation.origin == get_origin(py_type)
    arguments = get_args(py_type)
    assert type_annotation.arguments == (arguments[0],)
    assert type_annotation.metadata == tuple(arguments[1:])
    assert type_annotation.valid_base_type == arguments[0]


@pytest.mark.parametrize(
    "py_type,arguments",
    [
        (list[int], (int,)),
        (dict[str, int], (str, int)),
        (set[float], (float,)),
        (tuple[str, ...], (str, ...)),
    ],
)
def test_collections_with_arguments(py_type: type, arguments: tuple[type, ...]):
    type_annotation = TypeAnnotation.from_py_type(py_type)
    assert type_annotation.origin == get_origin(py_type)
    assert type_annotation.arguments == arguments
    assert type_annotation.metadata == ()
    assert type_annotation.valid_base_type == get_origin(py_type)


@pytest.mark.parametrize("py_type,arguments", [(list[int | float], (int | float,))])
def test_collections_with_union(py_type: type, arguments: tuple[type, ...]):
    type_annotation = TypeAnnotation.from_py_type(py_type)
    assert type_annotation.origin == get_origin(py_type)
    assert type_annotation.arguments == arguments
    assert type_annotation.metadata == ()
    assert type_annotation.valid_base_type == get_origin(py_type)


def test(py_type: Annotated[Annotated[int, "innter integer"], "outer annotation"]):
    ...
