---
date: 2020-05-19T19:45
tags:
  - programming
---

# Arithmetics Without Plus

There is a correspondence between natural numbers and types. Numbers can be assigned to types, according to how many values of a given type exist. If you know what I'm talking about, you can skip this section right to the [funky arithmetics](#funky-arithmetics).

For example, consider Python's types.

What about `bool`? It has two values ("*inhabitants*"): `True` and `False`. We can say that `bool` corresponds to 2.

$$\mathtt{bool}\sim2$$

Another example is `None`, which has a single inhabitant: `None`. Therefore, the `None` type corresponds to 1.

$$\mathtt{None}\sim1$$

What about a tuple `(bool, bool, bool)`? There are 8 = 2 \* 2 \* 2 possible triplets of `True` and `False`. This tuple type therefore corresponds to 8, which is a product of all the types inside.

$$\mathtt{(bool, bool, bool)}\sim8$$

These 8 values can be enumerated exhaustively:

```python
(False, False, False)
(False, False, True)
(False, True, False)
(False, True, True)
# four more values...
```

Tuples and structs are actually sometimes called **product types**, which reflects our little arithmetic. You can check for yourself that it works also with other type combinations.

So types correspond to **numbers**, and tuples/structs correspond to **products**. It would definitely have a much nicer ring to it if we also had **sums**. Turns out sum types exist, but not in all programming languages. They are commonly known as tagged unions. But there's no fun in those. Let's start with something most programming languages actually have: **nullable types**. Also known as the [billion dollar mistake](https://en.wikipedia.org/wiki/Tony_Hoare#Apologies_and_retractions).

Say we have a non-nullable type with `a` inhabitants. If we make it nullable, we have one extra value to put inside: `null`. The type becomes `a + 1`. There is our first sum type. For example, all Java objects are nullable.

$$\mathtt{Object}\sim a + 1,$$

where $a$ is the number of inhabitants of `Object`. This reflects the fact that the variable of type `Object` can be either `null`, or a proper instance. This pattern is commonly used for error handling. In case an operation fails, a `null` is returned.

There is, however, a problem with this approach. One error value often isn't enough. We really want a function to be either a value, or an error. Both of these may be complicated types. This is a common requirement, and also precisely what **sum types** are for. Let's invent a hypothetical syntax for them. The return value of a parser may be for example `Result | String`, signifying that the parser returns either `Result`, or a `String` with an error message. The `Result | String` type has all the inhabitants from both constituent types.

$$\mathtt{Result} \sim a$$

$$\mathtt{String} \sim b$$

$$\mathtt{Result\:|\:String} \sim a+b$$

That "+" above is why it is called a "sum type".

## Funky Arithmetics

How do mainstream languages realize this pattern of returning either X, or Y without the support for proper sum types? By doing some funky arithmetics with product types, of course. In other words:

<div style="text-align: center; border: 1px solid black; margin: 1em; padding: 1em; font-style: italic;">How do you add numbers, when all you know is multiplication?</div>

This obviously can't be done precisely. But we can afford to be imprecise. We only need the sum type equivalent to $a+b$ to be representable by our hypothetical multiplication-based type equivalent to, say, $n$. In other words:

$$n\geq a+b.$$

Let's see what we can do.

**Answer 1:** Try multiplying instead, hope it works.

It doesn't work, unfortunately. $a\cdot b\ngeq a+b$. Not all is lost, though! How about multiplying some more? The smallest extra thing we can multiply by is 2.

$$2ab=ab+ab.$$

We got a nice summation by expanding the expression. With a bit of imagination (a > 0, b > 0), we can arrive at this conclusion:

$$2ab=a+b+w,$$

where $w$ is a non-negative number, also known as `stuff_nobody_cares_about`. Let's decipher what type $2ab$ corresponds to. In our parser example ( $\mathtt{Return}\sim a,\mathtt{String}\sim b$ ), it would be:

$$\left(\mathtt{bool,\:Result,\:String}\right)\sim2ab.$$

It is very easy to see how this emulates a sum type. The `bool` value tells whether we got a `Result`, or a `String`. There is always one unused value (`Result` in case of error, and *vice versa*), it is the stuff nobody cares about.

In languages like C where returning multiple values is clunky, you can use output parameters for `Result` and `String`, and return the `bool` as a function result.

**Answer 2:** Profit from the billion dollar mistake.

We got the add-one operation for free in most languages in the form of nullability. What happens if we multiply two nullable values?

$$\left(a+1\right)\left(b+1\right)=a+b+\underset{w}{\underbrace{ab+1}}.$$

That is $a+b$, plus some extra stuff $w$ (nobody cares about). The `null` values are used to determine which type we got.

This pattern is common in many languages. Notably, it is idiomatic in Go. Functions return the pair `value, err`, and then use the error's `nil` value to tell whether we should care about one or the other.

**Answer 3:** Who needs infinities?

If the number of error conditions $b$ is small enough, we can represent them all inside an `int`. There may  even be enough space inside `int` to signalize whether the error occurred or not.

$$\mathtt{Result} \sim a$$

$$\mathtt{int} \sim 2^{32}$$


$$\left(\mathtt{Result,\:int}\right)\sim2^{32}\cdot a$$

Let's split off one value from the `int` to signalize the error ($b\leq2^{32}-1$):

$$2^{32}\cdot a\geq\left(b+1\right)\cdot a=a+ab=a+b+w,$$

for $a>0$, and a non-negative thing <sup><sup>(nobody cares about)</sup></sup> $w$.

This pattern is ubiquitous in Unix return codes, and in C, where errors are frequently represented by return codes/numbers/enums.

**Answer 4:** Pretend there are no sum types.

Functions just return values. If there is an error, they ... don't return at all? Maybe they could use a different, exceptional mechanism for error handling? Maybe the error value could be propagated using a different code-path, and be caught somewhere else, separately?

## Conclusion

There are many ways to emulate summation with multiplication. The list above isn't exhaustive, you can probably come up with your own ideas. And I guarantee that all of them will be as rubbish as the ones I listed. I leave it as an exercise to figure out what is wrong with each approach. Those problems are well-known within the industry.

There is really no good reason not to use sum types. They can be very efficient ([Rust](https://www.rust-lang.org/)), and they have been around since the 1970s ([Hope](https://en.wikipedia.org/wiki/Hope_(programming_language))).

And still, languages refuse to admit that summation is just as useful as multiplication.

Using such languages is like driving a car that only turns left. You can still go right by turning 270°, but it is annoying and sometimes you fall in a ditch along the way.
