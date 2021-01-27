---
date: 2020-12-24T11:35
tags:
 - programming
---

# Representing Effects using Pure Functions

Pure function has the following properties:

1. Its return value is the same for the same arguments.
2. Its evaluation has no side effects.

This means that pure functions are deterministic, and their execution is observable only through the return value. This disallows, for example, random number generation and file manipulations. This blog post details how these can be achieved using only pure functions.

# Random number generation

We can't generate random numbers in a pure function, period. Say we have this impure Javascript function:

```js
int rand() {

}
```

# This is not pure, can't have that!
def random():
    return math.random()

# This has side effects, can't do either
def print(x):
    sys.out(str(x))

# using the impossible functions to build something useful
x = random()
print(x)


def chain(f, g):
    x = f()
