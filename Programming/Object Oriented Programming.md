---
date: 2020-10-07T13:26
tags:
 - programming
---

# Object Oriented Programming

ZeroMQ author on why [choosing C++ over C was a mistake](https://250bpm.com/blog:4/).

OOP languages generally don't support failure in constructors and destructors. This leads to partially-initialized object states, which makes correctness hard.

> I believe that requirement for fully-defined behaviour breaks the object-oriented programming model.

# Side Effects

Uncle Bob (2008), of all people, trashes side effects, including changes to class member variables:

> Side effects are lies. Your function promises to do one thing, but it also does other hidden things. Sometimes it will make unexpected changes to the variables of its own class. Sometimes it will make them to the parameters passed into the function or to system globals. In either case they are devious and damaging mistruths that often result in strange temporal couplings and order dependencies.

## See Also

* [[OOP Deconstruction|OOP Deconstruction]]
* [[Functional Programming|Functional Programming]]