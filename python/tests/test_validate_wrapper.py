from typing import Annotated

from talk.validator import validate_annotated


@validate_annotated
def demo_function(a: Annotated[int, "test"], b: str):
    print(type(a))


def test_wrapper():
    demo_function(1, b="a string")


if __name__ == "__main__":
    test_wrapper()
