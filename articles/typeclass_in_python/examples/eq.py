from typing import Generic, TypeVar

from sparrow.kind import Kind, kind_function

T = TypeVar("T")


class Eq(Generic[T], Kind):
    @kind_function(True)
    def eq(self: "Eq[T]", other: "Eq[T]"):
        return not self.neq(other)

    @kind_function(True)
    def neq(self: "Eq[T]", other: "Eq[T]"):
        return not self.eq(other)


def same(a: Eq[T], b: Eq[T]) -> bool:
    return a.eq(b)


class IntEq(Eq[int]):
    def __init__(self, value: int):
        self.value = value

    def eq(self, other: Eq[int]):
        return self.value == other.value


same(IntEq(1), IntEq(1))  # True
same(IntEq(1), IntEq(2))  # False
