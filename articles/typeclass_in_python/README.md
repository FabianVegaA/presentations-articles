# Typeclass in Python using Sparrow

In the last time I've been working on a library called Sparrow. This library born from the need to have a collection of tools to make easier the development in Python using a more declarative approach, mainly in the composition of functions. Here I've created a collection of functions and decorators, and I've also implemented Typeclass inspired by Haskell.

## What is a Typeclass?

The concept of Typeclass is a very powerful tool in Haskell this allow us to create types of types. This is a way to use polymorphism using types. In Haskell we can define a Typeclass like this:

```haskell
class Eq a where
    (==) :: a -> a -> Bool
    a == b = not (a /= b)

    (/=) :: a -> a -> Bool
    a /= b = not (a == b)
```

In above example it defines Eq as a "type of types" for compare the equality of two values. The awesome thing about this is that we can define for example that the arguments of the function are of type Eq and the compiler will check if the types of the arguments have the Eq typeclass. So we can do generic functions like this:

```haskell
same :: (Eq a) => a -> a -> Bool
same a b = a == b
```

This function will work for any type that has the Eq typeclass.

Using Sparrow we can the same in Python:

```python
from sparrow.kind import Kind, kind_function

class Eq(Kind):
    @kind_function(has_default=True)
    def eq(a, b):
        return not a.neq(b)

    @kind_function(has_default=True)
    def neq(a, b):
        return not a.eq(b)


def same(a: Eq[T], b: Eq[T]) -> bool:
    return a.eq(b)
```

You can see that the definition of this type of type (I'll refer to it as kind) is very similar in both languages using Sparrow. The main difference is that in Python we need to use a decorator to define the polymorphic functions and specify if the function has a default implementation.

## How to use it?

This library offers the possibility of do data modeling. This means that we can model our system using types and functions. This is a very powerful tool because we can use the power of the type system to make our code more robust and easier to understand.

Let's see an example.

```python
from sparrow.kind import Kind, kind_function
from sparrow.datatype import DataType

class Speaker(Kind):
    @kind_function
    def speak(speaker: Speaker):
        pass

class Runner(Kind):
    @kind_function(has_default=True)
    def start_running(runner: Runner) -> None:
        print("I'm running")

    @kind_function(has_default=True)
    def stop_running(runner: Runner) -> None:
        print("I'm not running")

class Animal(Speaker, Runner, DataType):
    pass

class Dog(Animal):
    def speak(self):
        print("Woof woof")

class Cat(Animal):
    def speak(self):
        print("Meow...")

    def start_running(self):
        print("I'm a cat, I won't run")

    def stop_running(self):
        print("You can't stop me")

dog = Dog()
cat = Cat()

dog.speak() # Woof woof
cat.speak() # Meow...

dog.start_running() # I'm running
dog.stop_running() # I'm not running

cat.start_running() # I'm a cat, I won't run
cat.stop_running() # You can't stop me
```

This is not something new, we can do the same in Python using inheritance. But the difference is that a typeclass is a more declarative way to do it. We can see that the code is more readable and we can see the relationship between the types. And it doesn't matter if we use inheritance or not, the type system will work the same, but the focus is on the types.

### Error handling

In languages like Python, Java, and C# we have exceptions. This is a very powerful tool to handle errors. But every time we need to handle an error we need to use a try-catch block. And if the method or function returns a value we need to check if the value is a None, doing more complex the code. For example:

```python
def divide(a: int, b: int) -> int:
    return a / b

try:
    result = divide(10, 2)
except ZeroDivisionError:
    do_something()
```

In this case, we can refactor the code to use a Functor, specifically the Result type to handle the Exception. This is a very common pattern in functional programming. We can do it like this:

```python
from sparrow.datatype.result import Result, Success, Failure

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Failure("Division by zero")
    return Success(a // b)

divide(10, 0) # Failure("Division by zero")
divide(10, 2) # Success(5)
```

Or better:

```python
from sparrow.decorator.wrap import result

@result
def divide_v2(a: int, b: int) -> Result[int, Exception]:
    return a // b

divide(10, 0) # Failure(ZeroDivisionError)
divide(10, 2) # Success(5)
```

Now if we want to use the result we can simply map the value.

```python
result = divide(10, 0) # Failure(ZeroDivisionError)
result.fmap(lambda x: x * 2) # Failure(ZeroDivisionError)
```

And with other values:

```python
result = divide(10, 2) # Success(5)
result.fmap(lambda x: x * 2) # Success(10)
```

Inclusive we can compose more operations:

```python
result = (
    divide(10, 2) # Success(5)
    .fmap(lambda x: x * 2) # Success(10)
    .fmap(lambda x: x + 1) # Success(11)
    .fmap(lambda x: x % 2) # Success(1)
    .fmap(lambda x: "Even" if x == 0 else "Odd") # Success("Odd")
).value # "Odd"
```

Result also is a Bifunctor and we can use first, second, and bimap to map the first, second, or both possible values.

```python
result = divide(10, 0) # Failure(ZeroDivisionError)
result.first(lambda x: x * 2) # Failure(ZeroDivisionError)
result.second(lambda x: repr(x)) # Failure("ZeroDivisionError()")
result.bimap(lambda x: x * 2, lambda x: repr(x)) # Failure("ZeroDivisionError()")
```

Here the definition of Functor and Bifunctor is not relevant, these are just functional patterns and in this case, we are using them to handle errors.

### Maybe

Maybe is other type that Sparrow offers by default. This type is used to handle the None value. This is a very common pattern in functional programming. We can do it like this:

```python
from sparrow.datatype.maybe import Maybe, Just, Nothing

def divide(a: int, b: int) -> Maybe[int]:
    if b == 0:
        return Nothing()
    return Just(a // b)

divide(10, 0) # Nothing()
divide(10, 2) # Just(5)
```

Or if we prefer to use the decorator:

```python
from sparrow.decorator.wrap import maybe

@maybe
def divide(a: int, b: int) -> Optional[int]:
    return a // b if b != 0 else None

divide(10, 0) # Nothing()
divide(10, 2) # Just(5)
```

The decorator will map an optional return value to a Maybe type.

Maybe is a Functor, Applicative, and Monad. This means that we can use fmap, apply, and bind.

```python
result = divide(10, 2) # Just(5)
result.fmap(lambda x: x * 2) # Just(10)
result.apply(Just(lambda x: x * 2)) # Just(10)
result.bind(lambda x: Just(x * 2)) # Just(10)
```

Also, the Maybe has a method called `pure` that is used to create a Just value.

```python
from sparrow.datatype.maybe import Maybe

Maybe.pure(1) # Just(1)
```

> The `pure` function can be used by any type that implements the Applicative typeclass.

## Others tools

Sparrow also offers other functions tools. Here some examples:

### Currying

Currying is a technique to transform a function with multiple arguments into a function with a single argument. This is very useful when we want to use partial application. For example:

```python
from sparrow.decorator.currify import currify

@currify
def add(a: int, b: int) -> int:
    return a + b

add_one = add(1) # A function with one argument
add_one(2) # 3
```

### Composition

Composition is a technique to combine two or more functions.

```python
from sparrow.decorator.compose import compose

@compose(lambda x: x * 2, lambda x: x + 1)
def add_one_and_double(x: int) -> int:
    return x

add_one_and_double(1) # 4
add_one_and_double(2) # 6
```

The idea is to make pipelines of functions with more easily to modularize the code.

### Reflex

Reflex is intended to debug the code or produce a side effect to finish the execution.

```python
from sparrow.decorator.reflex import reflex

@reflex(lambda x: print(x))
def add_one(x: int) -> int:
    return x + 1

add_one(1)
# stdout: 2
```

If we want to debug we can use debug, info, warning, error, and critical decorators.

```python
from sparrow.decorator.reflex import debug, info, warning, error, critical

@critical
@error
@warning
@info
@debug
def add_one(x: int) -> int:
    return x + 1

add_one(1)
# stdout:
# DEBUG:root:2
# INFO:root:2
# WARNING:root:2
# ERROR:root:2
# CRITICAL:root:2
```

Also we can format the message.

```python
from sparrow.decorator.reflex import info

@info("The value is {0}")
def add_one(x: int) -> int:
    return x + 1

add_one(1)
# stdout: INFO:root:The value is 2
```

### Before and After

Before and after are decorators to execute a function before or after the execution of the decorated function.

```python

from sparrow.decorator.before_after import before, after

@after(str)
@before(int)
def add_one(x: int) -> int:
    return x + 1

add_one(1.1) # "2"
```

### When

#### The decorator

When is a decorator to execute a function when a condition is true.

```python

from sparrow.decorator.when import when

@when(lambda x: x > 0)
def add_one(x: int) -> int:
    return x + 1

add_one(1) # 2
add_one(-1) # -1
```

#### The function

When is also a function to execute a function when a condition is true.

```python
from sparrow.function.when import when

def divide(a: int, b: int) -> int:
    return when(
        condition=b != 0,
        then=lambda x: x / b,
        otherwise=lambda x: 0,
        value=a
    )

divide(10, 2) # 5
divide(10, 0) # 0
```

#### Map when

Map when is a function to execute a function when a condition is true and map the result.

```python
from sparrow.function.when import map_when

my_list = [1, 2, 3, 4, 5]

map_when(
    condition=lambda x: x % 2 == 0,
    then=lambda x: x * 2,
    value=my_list
) # [1, 4, 3, 8, 5]
```

## Conclusion

All tools must be used with caution and preferably with a strict type checking. The purpose of this library is to help you to write more declarative code, and flexibility the data modeling and composition of functions.

This library is still in development, and I am open to suggestions and contributions. The repository is available on [GitHub](https://github.com/FabianVegaA/sparrow). The documentation is not available yet, but I am working on it.
