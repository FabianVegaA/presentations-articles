def divide(a: int, b: int) -> int:
    return a / b

def do_something():
    print("Something")

try:
    result = divide(10, 0)
except ZeroDivisionError:
    do_something()