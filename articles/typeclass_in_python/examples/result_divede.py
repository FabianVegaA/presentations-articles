from sparrow.datatype.result import Result, Success, Failure


def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Failure("Division by zero")
    return Success(a // b)


print(divide(10, 0))  # Failure("Division by zero")
print(divide(10, 2))  # Success(5)

from sparrow.decorator.wrap import result


@result
def divide_v2(a: int, b: int) -> Result[int, Exception]:
    return a // b


print(divide_v2(10, 0))  # Failure(ZeroDivisionError(...))
print(divide_v2(10, 2))  # Success(5)

result = divide_v2(10, 0) # Failure(ZeroDivisionError)
print(result.fmap(lambda x: x * 2)) # Failure(ZeroDivisionError)

result = divide(10, 2) # Success(5)
print(result.fmap(lambda x: x * 2)) # Success(10)

result = (
    divide(10, 2) # Success(5)
    .fmap(lambda x: x * 2) # Success(10)
    .fmap(lambda x: x + 1) # Success(11)
    .fmap(lambda x: x % 2) # Success(1)
    .fmap(lambda x: "Even" if x == 0 else "Odd") # Success("Odd")
).value # "Odd"

print(result)

result = divide_v2(10, 0) # Failure(ZeroDivisionError)
print(result.first(lambda x: x * 2)) # Failure(ZeroDivisionError)
print(result.second(lambda x: repr(x))) # Failure("ZeroDivisionError()")
print(result.bimap(lambda x: x * 2, lambda x: repr(x))) # Failure("ZeroDivisionError()")