---
date: 2022-02-28T12:59
tags:
  - programming
---

# Bugs I Introduced

While programming in Haskell. Haskell has a strong type system which prevents many bugs. These are the bugs that I managed to create in spite of that.

I'm not discussing the exact bugs, but rather their causes.

* One bug was caused by using two different representations for zero. Only one of them was properly tested. A bug in handling the other one was therefore not detected. The two representations were:

  1. A missing key in a `Map Int _`,
  2. A zero key in the same map.

  A solution would've been to use a `TotalMap` instead, which models the logic more tightly.

* Another bug was a problem in my understanding of specification. The bug would've been caught by 3 tests, but these were also written according to the bad specification.

* Another bug was caused by a list being produced in a reversed order by a recursive function. This was not very obvious from the function definition. It sneaked through the tests as well, and landed in production.
