from sparrow.kind import Kind, kind_function
from sparrow.datatype import DataType
from dataclasses import dataclass

class Speaker(Kind):
    @kind_function
    def speak(speaker: "Speaker"):
        pass

class Runner(Kind):
    @kind_function(has_default=True)
    def start_running(runner: "Runner") -> None:
        print("I'm running")

    @kind_function(has_default=True)
    def stop_running(runner: "Runner") -> None:
        print("I'm not running")

class Animal(Speaker, Runner, DataType):
    pass

@dataclass
class Dog(Animal):
    def speak(self):
        print("Woof woof")

@dataclass
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