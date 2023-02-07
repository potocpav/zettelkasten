---
date: 2020-11-30T16:57
tags:
 - programming
---

<style>
body {
    font-size: 1.1em !important;
}
</style>

# Functional Programming

Functional programming (FP) is, similarly to other programming paradigms, quite difficult to pin down. Instead of having a clear definition, these characteristics are commonly associated with functional style:

* **Functions are treated as first-class citizens.** They are frequently passed as arguments to other functions.
* **Functions are pure.** They are deterministic and side-effect-free, similarly to mathematical functions.
* **Algebraic data types** are used for data modelling.
* **Immutable values** are preferred over mutable values.
* **Algebraic structures** are used as abstractions.

Seeing the value of these characteristics is not easy, however. Each of them must be argued separately, and it can be difficult to make a solid case for their utility, especially to a person who is used to programming in a different paradigm. How can we convince fellow developers that all the functional weirdness is warranted? I will try to present an unified argument for all the FP characteristics in this article.

It turns out that all of the above points can be derived from a single design rule.

<style>
.banner {
    font-size: larger;
    padding: 0.5rem;
    margin: 1rem;
    border: 1px solid black;
    text-align: center;
}
</style>
<p class="banner">
Functional programming is the consequence of using types to precisely encode program semantics.
</p>

If you agree that type systems should be used to their full potential, functional programming is not much of a paradigm - it is rather just a natural consequence. And it is quite uncontroversial to see that type systems should be wielded efficiently to prevent bugs and maximize correctness. That's, after all, precisely what they were designed to do in the first place.

Note that the above statement is an implication:

$$\text{precise types} ⇒ \text{functional programming}.$$

The converse isn't true, as FP is also possible in weakly-typed languages:

$$\text{functional programming} ⇏ \text{precise types}.$$

In the following sections, I will try to show how each of the signature FP features serves to make types more precise.

## Algebraic Data Types

Data types allow us to specify what values an expression might take. We want types to match semantics as precisely as possible. They would ideally allow all valid values while disallowing all invalid values. Algebraic data types (ADTs) provide us with a rich vocabulary to construct precise types in many scenarios.

For example, say we want to specify a type representing a JSON value.

```c++
// This is a JSON value.
JSON json;
```

What we don't want is a JSON value with a fine print attached:

```c++
// This is a JSON value¹
// ¹ or an inconsistent thing with undefined behavior on access
JSON json;
```

We can have a look at how this is acnieved in practice. Here is how one might represent a JSON value in C++. Code is adapted and simplified from the popular [nlohmann's JSON library](https://github.com/nlohmann/json):

```c++
enum class value_t {
    null, boolean, number_float, integer, string, array, object,
};

union json_value {
    bool boolean;
    double number_float;
    std::int64_t number_integer;
    std::string *string;
    std::vector<json> *array;
    std::map<std::string, json> *object;
}

class json {
    value_t m_type;
    json_value m_value;
}
```

Consider what needs to be ensured for `json` to represent a valid JSON value:

1. `m_type` must be an integer less than 7.
2. `m_type` must correspond to the type of `m_value`.
3. For a string, array, and object, `m_value` must be a valid pointer.
4. Above points must be satisfied on all depth levels, since `json` is a tree structure.

These requirements are commonly known as **invariants**, and they are precisely the **rules that aren't captured by the type system**; they must be upheld by the programmer. Indeed, the `json` library [documents some of them in comments](https://github.com/nlohmann/json/blob/97fe455ad5dd889ed30cf23bc735bb038ef67435/include/nlohmann/json.hpp#L150-L155) and provides [functions to check their validity](https://github.com/nlohmann/json/blob/97fe455ad5dd889ed30cf23bc735bb038ef67435/include/nlohmann/json.hpp#L1227-L1233). To further facilitate safety, `m_type` and `m_value` are private, so only the code inside the JSON library must be careful about invariants.

This is a compromise rather than the ideal case. We must trust library internals to correctly uphold all the invariants. Nlohmann's JSON library contains thousands of lines of code with access to the private fields of `json`, so this is definitely not a trivial concern!

Invariants arise from the inability of the type system. If we were able to construct a type which contains **only** valid JSON values, all these problems would disappear. We could expose data directly, since every value is valid by construction. There is no longer a trusted code-base, no assertions, tests or comments about invariants, we only need to trust the type-checker.

Behold the Rust JSON representation, adapted from the canonical [serde library](https://github.com/serde-rs/json):

```rust
pub enum Json {
    Null,
    Bool(bool),
    Integer(i64),
    Float(f64),
    String(String),
    Array(Vec<Json>),
    Object(Map<String, Json>),
}
```

Rust `enum` is an union type which contains precisely one of the specified alternatives:

* Either a `Null`,
* or a `Bool` with a single `bool` value,
* or an `Integer` with an `i64` value,
* etc.

Notice how the `Json` enum is public. It can be, because there are no invariants. It is impossible to construct invalid `Json` values. Rust enumerations, which are an example of an algebraic data type, enable us to model semantics much more precisely than plain structs. This shifts responsibility from the programmer to the type checker, and allows us to write more reliable software. Here I showed just one example, but surprisingly many different objects can be precisely described using ADTs.

ADTs are one way to precisely model type semantics. Without proof[^1], I will assert that they are actually the **only** way: you need a feature of (at least) equivalent power to hope for precise types. This would mean that we have the first piece of the puzzle:

<p class="banner">
<b>ADTs</b> are the consequence of using types to precisely encode program semantics.
</p>

## Pure Functions

Continuing the example from the previous section, let's define a function in Rust which returns a string represented by the given JSON:

```rust
fn to_array(json: Json) -> Option<String> {
    match json {
        String(s) => Some(s),
        _ => None,
    }
}
```

This function works correctly for any `json` no matter what it is, or where it came from[^2]. Can we have similar guarantees for function types too? Let's examine Java `map` combinator for the Stream interface.

```java
/*
* Returns a stream consisting of the results of applying the given
* function to the elements of this stream.
*
* @param <R> The element type of the new stream
* @param mapper a non-interfering, stateless function to apply to each element
* @return the new stream
*/
<R> Stream<R> map(Function<? super T, ? extends R> mapper);
```

The `map` method takes the function `mapper` to produce a transformed stream of values. Does `map` work for correctly for any choice or `mapper`? No. This fact is duly stated in the comment above: `mapper` must be a "[non-interfering, stateless function](https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html#NonInterference)". If this condition is not satisfied, bad stuff can happen including data races, exceptions, and incorrect or non-deterministic results. We have once again found an imprecise type which is inhabited by more values than are semantically valid. We have to rely on our diligence to ensure that the invariants hold.

Let's take a step back and examine why this is the case. The type of a function, called **function signature**, consists of **argument types** and the **return type**[^3]. Argument types specify the prerequisites, and the return type specifies the results of the function. However, there are escape hatches: functions can also perform various side-effects not captured by the signature. They can typically

* Access global variables, static variables, or instance variables,
* Access external resources such as PRNG state, network state, file IO, console, etc.,
* Mutate arguments,
* Throw exceptions.

These interactions must be well documented and kept in mind by the programmers since the type system cannot help us. If side effects are not used sparingly, function signatures lose their descriptiveness.

To fix the `map` example above, we must have a way to enforce the "non-interfering, stateless" property at the type level. We call this property **purity**, and pure functions interact with the outside world *exclusively* through their arguments and return types. Without purity, we can't assign precise types to higher-order functions: functions that use side effects to wreak havoc will always creep into our types.

We have no choice but to limit ourselves to pure functions, and it follows that

<p class="banner">
<b>Pure functions</b> are the consequence of using types to precisely encode program semantics.
</p>

Many languages nowadays allow marking pure functions as such: `const fn` in Rust, `constexpr` in C++, `pure` in D, etc. This capability tends to be, unfortunately, too limiting to be used for the types of higher-order function arguments. The only general-purpose languages that use pure functions pervasively are from the Haskell family. In Haskell, as a matter of fact, all functions are pure. And sure enough, no comments are needed in Haskell to specify how the mapping function should behave, as all functions of the correct type are valid.

```haskell
-- O(n). `map f xs` is the list obtained by applying
-- `f` to each element of `xs`.
map :: (a -> b) -> [a] -> [b]
```

## Algebraic Structures

Now we have precise value and function types, but that is not enough. We also need a way to specify relations between them. Consider, for example, a sorting algorithm. It consists of a function `sort` together with a less-or-equal operator `leq`. In pseudo-code:

```rust
sort(Array<T>) -> Array<T>
leq(T, T) -> Bool // less or equal, ≤
```

The correctness of `sort` depends crucially on the semantics of `leq`: it can't be any old function, it must be a [total order](https://en.wikipedia.org/wiki/Total_order). It must satisfy the following relations:

* **Antisymmetry**. If `a ≤ b` and `b ≤ a` then `a = b`.
* **Transitivity**. If `a ≤ b` and `b ≤ c` then `a ≤ c`.
* **Connexity**. `a ≤ b` or `b ≤ a`.

If some of these are not satisfied, `sort` behaviour may not be what we expect. In Python, for example, the following happens:

```python
>>> sorted([4, float('nan'), 2, 1])
[4, nan, 1, 2]
```

This result is clearly incorrect, and it is because `leq` is not a total order over IEEE 754 floats: it doesn't satisfy connexity. We need a way to encode this requirement into the type system, otherwise these kinds of bugs can't be prevented. This is what typeclasses/traits are used for. In Haskell:

```haskell
sort :: Ord a => [a] -> [a]
```

The `Ord` constraint tells us that we have `≤` which forms a total order over `a`. In Rust, there is an equivalent pattern, this time sorting in place:

```rust
impl<T> Vec<T> {
    pub fn sort(&mut self) where T: Ord,
}
```

And indeed, `Ord` is not implemented for floats, which prevents the pathological use-case above. Users of `sort` and orderable types can rest assured that they can't mess up the composition.

For a different example, suppose we want to make a parallel array sum function. This function splits the array into N sub-arrays, sums up each one in a thread, and finally sums the sub-results together. To get the same result regardless of the number of sub-arrays, our sum operation must be associative. We can express this by using the `Semigroup a` constraint which provides us with an associative operation over `a`.

```haskell
parallelSum :: Semigroup a => [a] -> a
```

We need to use algebraic structures, such as a semigroup or a total order, to precisely specify types of functions whose correctness depends on the satisfaction of specific laws relating values and functions. This is the conclusion:

<p class="banner">
<b>Algebraic structures</b> are the consequence of using types to precisely encode program semantics.
</p>

This pattern of having algebraic structures with associated laws is ubiquitous in functional programming, and there are many well-known algebraic structures. In OOP languages, interfaces or classes could be used to the same effect, however, they have [many restrictions](https://stackoverflow.com/a/8123973) which make them much less useful.

## Immutable Values

If we limit ourselves to only pure functions, mutability is no longer very useful. Functions can't access anything but their arguments, and those can't be modified. This means that mutability is confined only to function bodies, where it can serve as a convenience. Some languages use function calls instead of `for` and `while` loops, which prevents the few remaining use-cases for mutable values. Thus, immutability follows naturally from the other functional programming concepts we discussed earlier.

That said, mutable output arguments can be useful. I don't see a problem with this alternative, as long as they are explicitly marked. It doesn't weaken the expressiveness of function signatures and can be used, for example, to achieve greater performance. In Rust, mutable arguments are marked in the function signatures **and** at the call-sites, which makes information flow very obvious.

## Higher-order Functions

There is probably an argument for how common HOFs like `map`, `filter`, or `reduce` help enhance type safety, but this article is too long already so I'm going to take the easy way out.

The use of higher-order functions (HOFs) in functional programming can be seen as the consequence of the above features. Functional purity forces the use of HOFs to describe even simple concepts like sequential actions. And because of pure functions and algebraic laws, it is safe and pleasant to work with HOFs. This leads to HOFs being used pervasively in functional programming, and thus, being associated with functional style.

## Notes on OOP

Object oriented programming is a particularly bad offender when it comes to imprecise types, since it encourages both imprecise data types and non-descriptive functional signatures.

**Imprecise data types** arise because classes frequently contain too many fields which themselves are poorly typed. This is caused by:

* OOP mental model of "thing == instance" is often not granular enough.
* Inheritance brings unnecessary baggage.
* Uninitialized states [are sometimes unavoidable](https://250bpm.com/blog:4/).
* Nullability is pervasive in mainstream OOP languages.

Often, tons invalid states are possible in class instances, and keeping everything consistent is a **major** challenge.

**Non-descriptive functional signatures** are given by the fact that functions have blanket access to instance variables. This is the same as passing in a bunch of mostly unnecessary arguments, which goes against descriptive function types. Worse, functions may work mainly through instance state manipulation instead of through return values. This leads to non-descriptive types, and by trying to compensate, to overly descriptive names. Ever seen code that looks like this excerpt from Clean Code?

```java
private void includeSetupAndTeardownPages() throws Exception {
    includeSetupPages();
    includePageContent();
    includeTeardownPages();
    updatePageContent();
}

private void includeSetupPages() throws Exception {
    if (isSuite)
      includeSuiteSetupPage();
    includeSetupPage();
}

private void includeSuiteSetupPage() throws Exception {
    include(SuiteResponder.SUITE_SETUP_NAME, "-setup");
}

private void includeSetupPage() throws Exception {
    include("SetUp", "-setup");
}
```

Notice how function signatures are devoid of any information - every function has the exact same signature! Any of the statements can be duplicated, deleted, or rearranged without the compiler complaining. Control flow is fully implicit and the type system is all but useless. Luckily, this hardcore OOP style [is on the decline](https://qntm.org/clean).

In a purely functional setting, this can't happen. Any pure function which returns `void` is useless since it conveys no information in its return value. As a rule of thumb, even in a non purely functional setting, `void`-returning functions should probably rarely be used.


## Conclusion

We have seen how different characteristics of functional programming arise from insisting on descriptive types. The main take-away is that functional programming does one thing better than other approaches: it better utilizes the type system.

This doesn't mean that FP is overall better for software development. Perhaps in the process of being pedantic with types we arrived at a paradigm that is too impractical for everyday use. Discussing whether this is the case, and showing how effectful systems can be written in a purely functional style, may be the topic of a future blog post.

[^1]: If I'm wrong on this, please point it out in the comments.
[^2]: C++ equivalent could exhibit undefined behavior if some of the invariants were broken.
[^3]: There is typically more information such as checked exceptions, value mutability, etc.

## See Also

* [[OOP Deconstruction|OOP Deconstruction]]
* [[Object Oriented Programming|OOP Notes]]
