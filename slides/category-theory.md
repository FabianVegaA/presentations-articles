---
theme: default
paginate: true
title: Category Theory
marp: true
---

# Category Theory

This is a branch of mathematics that uses the concept of a category to study the relationships between objects and morphisms.

---

I going to talk about the following topics:

- What is a category? And its components
- What is a monoid?
- What is a functor?
- What is a natural transformation?
- What is a monad?
- Applications of category theory

---

# What is a category?

A category is a collection of objects and morphisms between them.

## Objects

Objects are the things we are interested in. They are the nouns of our domain. For example, in the category of sets, the objects are the sets. Also, we can work with types in the category of types.

## Morphisms

Morphisms are the arrows between objects. They are the verbs of our domain. For example, in the category of sets, the morphisms are the functions that map from one set to another.

---

# Monoid

A monoid is a category with a single object and a single morphism.

## Identity morphism

The identity morphism is the morphism that maps from the object to itself. It is the identity function in the category of sets.

![bg right:50% 70%](https://bartoszmilewski.files.wordpress.com/2014/12/monoid.jpg?w=472&h=600)

---

# Functor

A functor is a mapping between categories. 

## Functor laws

- Identity: `fmap id = id`
- Composition: `fmap (f . g) = fmap f . fmap g`

> In languages as Haskell, the `fmap` is used to map over a functor.

---

# Natural transformation

---

# Monad

---

# Applications of category theory

The main application of category theory is in functional programming. It is used to study the relationships between functions and their composition. And for example, Haskell is a pure functional language that uses category theory to describe its type system, this allows us to write pure functions manipulating data without side effects.

---

# References

- [Category Theory for Programmers](https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/)