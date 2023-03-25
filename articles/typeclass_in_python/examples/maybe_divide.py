from sparrow.datatype.maybe import Maybe, Just, Nothing

def divide(a: int, b: int) -> Maybe[int]:
    if b == 0:
        return Nothing()
    return Just(a // b)

print(divide(10, 0)) # Nothing()
print(divide(10, 2)) # Just(5)

from sparrow.decorator.wrap import maybe
from typing import Optional

@maybe
def divide(a: int, b: int) -> Optional[int]:
    return a // b if b != 0 else None

print(divide(10, 0)) # Nothing()
print(divide(10, 2)) # Just(5)

result = divide(10, 2) # Just(5)
print(result.fmap(lambda x: x * 2)) # Just(10)
print(result.apply(Just(lambda x: x * 2))) # Just(10)
print(result.bind(lambda x: Just(x * 2))) # Just(10)

from sparrow.datatype.maybe import Maybe

print(Maybe.pure(1)) # Just(1)