---
date: 2020-05-01T14:30
tags:
  - programming
---

# Designing a GUI Framework

Designing UI libraries is hard. System integration, accessibility, styling, those are difficult to do properly. But this article is about something much harder. Designing a good UI from the developer's point of view.

Here is a fun fact: **developers hate writing user interfaces**. For good reasons: it is difficult, time-consuming and boring. That's why most personal projects are text-based, even though a GUI would perhaps be a better fit. Is UI programming really that difficult? Or do GUI frameworks make it harder than it needs to be?

In this article, I will argue that the latter is true: it's not inherently difficult to write GUIs, if you have the right toolset. I will dive into the design rationale behind such a toolset, **Concur**. Concur enables you to write complex applications, as well as write quick throw-away GUI scripts, in much the same way you would write console scripts in Python. With Concur, simple applications can be written just in a few lines of code, and complex applications are just as difficult as they need to be, not more.

# Problem Analysis

To understand how to create an GUI framework, we must carefully analyze the problem first.

User interfaces can be decomposed into atomic building blocks, **widgets** (aka elements, controls, components, etc.) These are the buttons, text boxes, windows, etc. Widgets are **composed** to form more complex components, which in turn form the whole application. This **widget composition** is where the complexity lies, and what makes GUI programming hard. Widgets are not just functions, or data structures - we can compose these quite easily. Widgets are **data structures with behavior** (i.e., OOP objects with methods), as they need to react to user input. Composing such entities in the right way is not a trivial problem.

There are actually two distinct types of composition: composition in space, and composition in time.

**Composition in space** is the one we commonly think of when we say "composition". We use it to display several widgets simultaneously. Composition in space is  tedious to do in code, and making it more natural is the goal of many GUI frameworks. We have designer tools, even whole languages dedicated to composition in space.

**Composition in time** is much less obvious. Conceptually, it is about displaying or modifying a widget *in reaction to interaction with another widget*. Often, we need to change the widget tree dynamically: in installation wizards, multi-page forms, mode-based applications, etc. But it is much more common than that - perhaps we need to enable/disable a text-box in reaction to some events. This can be also viewed as composition in time.

The above distinction can be stated more precisely:

**Composition in space**. Widget A exists simultaneously with widget B. There is no inherent order of definition, or dependency.

**Composition in time**. Future widget A depends on interaction with a past widget B. There is an enforced order: we can't create future widgets until we know the results of interaction with past widgets.

This is what [traditional](https://www.qt.io/) [UI](https://www.gtk.org/) [frameworks](https://en.wikipedia.org/wiki/Windows_Forms) get wrong. They **focus solely on composition in space**. They don't help you much with composition in time. How do you change user interface itself based on user interaction? You mostly do it via mutation triggered from event handlers. You change some widgets' properties, destroy one widget and create another, or change a part of application state. This ad-hoc nature of state evolution makes it really hard to reason about code. Stuff is changed in many random places, the order of change matters, and it is easy to end up in an inconsistent state. The application becomes a ball of spaghetti full of edge cases.

In other words: **composition in time is implicit**. And the problem is that time composition is actually the harder one of the two.

# Solution

Let's take a step back, and think about how we can solve these issues. The root of the problem is that **widgets can't be composed easily, because they are complex**. As we mentioned above:

* Widgets manage state.
* Widgets can be interacted with.

How can we simplify that? The guys over at front-end development showed us the way:

* ~~Widgets manage state.~~
* Widgets can be interacted with.

We can get rid of state management by **making widgets immutable**. Need to change button color? Throw the button out, create a new button. Need to add a character to a text field? Destroy the text field, create a new one. It's like a magician's trick: the apple seems to change into an orange, but really, it was just swapped behind the scenes. [Virtual DOM](https://en.wikipedia.org/wiki/React_(web_framework)#Virtual_DOM) makes this efficient.

As a matter of fact, we can simplify further. Now that we destroy & create widgets all the time, we can simplify user interaction too:

* ~~Widgets manage state.~~
* Widgets can be interacted with <span style="background-color: yellow">just once.</span>

After a widget is interacted with, it ceases to exist, and must be replaced by a different one.

All this may seem radical, but if it works, it actually brings nice separation of concerns. Widgets just do widget stuff, look nice, and wait for an interaction. They delegate all the time-related issues to separate primitives dealing with composition in time. Complexities related to displaying multiple widgets at once are likewise delegated to space composition primitives.
<!-- Layout-related issues are likewise delegated to space composition primitives. -->
These three sub-systems are fairly independent of one another.

## Let's Talk Composition

By minimizing responsibilities, we have arrived at the simplest widget type ever. Using Haskell syntax[^type_syntax], it is:

```haskell
Widget a
```

where the type `Widget` is parametrized by the (arbitrary) event type `a`.  A text box would be `Widget String`, a checkbox would be `Widget Boolean`, and a color picker would be `Widget Color`.

This reflects the fact that event type is the **only** thing we need to know about widgets to compose them. Otherwise, widgets are opaque to the rest of the program. They have no accessible state, no methods. Compared to object-oriented widget frameworks, this is simpler by [orders of magnitude](https://doc.qt.io/qt-5/qlist.html).

## Composition in space

How can we compose our widgets? We will discuss composition in space first, since it is the easier one. In the simplest form, we just take two widgets with two different event types (`Widget a`, and `Widget b`), and try to compose them into one. This type signature looks like a good start (again, using Haskell syntax[^function_syntax]):

```haskell
join :: Widget a -> Widget b -> Widget (Either a b)
--      ↳operand_1  ↳operand_2  ↳result
```

where `join` is the operator name, and `(Either a b)` is a tagged union (sum type) containing either `a`, or `b`. When `Widget a` is interacted with, we get `a`, When `Widget b` is interacted with, we get `b`. The resulting widget is even shorter-lived than its constituents, since it fires an event as soon as *any* child does. But the definition above has a flaw: it quickly leads to complicated types. If we try to compose a 5-element list, we get 5 different type parameters:

```haskell
x = join a (join b (join c (join d e)))
     :: Widget (Either a (Either b (Either c (Either d e))))
```

This is no good. The underlying issue is that the `join` operator does two unrelated things: it composes widgets, and it manipulates event types. These need to be separated into two functions, each serving a single orthogonal purpose:

```haskell
alt :: Widget a -> Widget a -> Widget a
map :: (a -> b) -> Widget a -> Widget b
```

`alt` composes only widgets with the same event type. `map` transforms event types using a user-supplied function `a -> b`. Now, we can recover `join` easily[^join], and the new approach is way more flexible. We can, for example, compose homogenous lists of widgets painlessly.

It turns out that this pattern of having `alt` and `map` is useful in general, and it already has a name: [`Alt`](https://hackage.haskell.org/package/semigroupoids-5.3.4/docs/Data-Functor-Alt.html#t:Alt). Our composition in space can be called the **alt composition**.

## Composition in Time

Let's now examine composition in time. As stated above, widgets that come later depend on the results of earlier widgets. Our composition operator will take two widgets, where the **second one is created from the result of the first one**. It returns yet another widget:

```haskell
bind :: Widget a -> (a -> Widget b) -> Widget b
--      ↳operand_1  ↳operand_2         ↳result
```

`bind` takes a widget and a function, and creates a composite widget, which does the following when displayed on screen:

1. First, `Widget a` is displayed, until it finishes by creating an event `a`.
2. With `a`, the function supplied as the second argument (`a -> Widget b`) is called. The result, `Widget b`, is obtained.
3. `Widget b` is displayed on screen.

The resulting widget has the event type `b`, which is the event type of the **second** widget. Event `a` is only used internally to generate `Widget b`, and it isn't visible to the user of the `bind` result. This is the reason we don't need to limit ourselves to a single event type, as we did with `alt`: our types remain simple regardless.

It turns out that this kind of composition is also useful in general, and it is called the [**monadic composition**](https://pursuit.purescript.org/packages/purescript-prelude/4.1.1/docs/Control.Bind#t:Bind).

# Putting it All Together

These are the fundamental building blocks for widget composition we are left with:

* `alt`: operator for composition in space,
* `map`: operator for event transformation,
* `bind`: operator for composition in time.

I think this looks rather elegant, almost forced by the nature of things. With a few simple orthogonal concepts, we can compose widgets in any way we want[^nesting].

Can we build useful UIs from our three LEGO bricks? Let me take a shortcut, and demonstrate by example. There are now four UI libraries implementing these ideas in four different languages:

* [Concur](https://github.com/ajnsit/concur) - The original, written in Haskell.
* [Purescript Concur](https://github.com/purescript-concur/purescript-concur-react) - Well-maintained Purescript implementation for front-end programming.
* [Concur JS](https://github.com/ajnsit/concur-js) - The first port to an imperative language.
* [Python Concur](https://github.com/potocpav/python-concur) - Python port using ImGui instead of a virtual DOM.

The first three variants are written by [ajnsit](https://github.com/ajnsit). He's the one who developed the idea. I created the Python implementation after seeing how pleasant working in Purescript Concur was, and getting envious that I couldn't use it in machine learning.

In the following paragraphs, I will show simple Concur usage examples in Purescript and Python. While [Purescript](https://www.purescript.org/) (a Haskell-like language) is not familiar to many, it illustrates the concepts described above in a clearer way. Python is more familiar, but it uses Concur concepts in fairly un-obvious ways, as language limitations have to be worked around.  Feel free to [skip the Purescript example](#python-example) if it doesn't seem comprehensible.


# Purescript example

A simple counter widget in Purescript:

```haskell
1  import Prelude
2  import Concur.Core (Widget)
3  import Concur.React (HTML)
4  import Concur.React.DOM as D
5  import Concur.React.Props as P
6
7  counterWidget :: ∀ a. Int -> Widget HTML a
8  counterWidget count = do
9      n <- D.div'
10         [ D.p' [D.text ("State: " <> show count)]
11         , D.button [P.onClick] [D.text "Increment"] $> count+1
12         , D.button [P.onClick] [D.text "Decrement"] $> count-1
13         ]
14     counterWidget n
15
16 main = runWidgetInDom "main" (counterWidget 0)
```

Let's start from the middle:

```haskell
11         , D.button [P.onClick] [D.text "Increment"] $> count+1
```

This line creates a `button` widget, which reacts to the `onClick` event, and contains the text `"Increment"`. Quite self-explanatory. The `$>` operator is a `map` in disguise. It throws away the button's event type (a structure representing the onClick event), and replaces it with `count+1`, which is a simple `Int`. The result of the whole line is a button widget with type `Widget Int`.

A second line we will look at is this one, creating a  paragraph with the counter value:

```haskell
10         [ D.p' [D.text ("State: " <> show count)]
--                                    ↳ text concatenation
```

This paragraph doesn't emit any events (it is passive), and just shows a given text. What is the type of a passive widget? Since the event is never observed (none is ever created), it could be literally anything. We can write this fact as the type `∀ a. Widget a`.

We now construct a `<div>` from the widget list:


```haskell
9      n <- D.div'
10         [ D.p' [D.text ("State: " <> show count)]
11         , D.button [P.onClick] [D.text "Increment"] $> count+1
12         , D.button [P.onClick] [D.text "Decrement"] $> count-1
13         ]
```

where three widgets are composed with types `∀ a. Widget a`, `Widget Int`, and `Widget Int`. The type checker resolves `a = Int`, so everything is of the same type. The list is finally composed into a single widget by `D.div'` (internally using `alt`[^conceptually]), and immediately wrapped inside a `<div>`.

The `<-` operator (line 9) waits for an event to be created by `D.div'`, and assigns it to a variable `n` which can be used on the following lines. This is the composition in time. It is implemented in terms of `bind`, but not explicitly, since monadic composition is so common that is has language support in Purescript ("do-notation")[^bind].

Finally, `n` is used in a recursive call to `counterWidget`:

```haskell
16   counterWidget n
```

This is how we create a never-ending widget from our otherwise short-lived building blocks. Had this call not been here, the application would exit after a single interaction.

So the whole `counterWidget` exists forever: it doesn't, as a single unit, fire any events. This is, similarly to the text-widget, reflected in the type, which is universally quantified:

```haskell
6  counterWidget :: ∀ a. Int -> Widget HTML a
--                                     ^^^^ ignore me
```

Now that all the building blocks have been composed into a single `Widget`, our application is finished and it can be displayed on screen by calling:

```haskell
16 main = runWidgetInDom "main" (counterWidget 0)
```

# Python example

In the Purescript example, many advanced language features were used to make it all work painlessly. Things like the do-notation are not present in mainstream languages, including Python. Can we make it work nevertheless? Turns out we can, by abusing the language a little.

Python has a permissive type system, so the shenanigans we did with universal quantification do not really pose a problem.

What **is** a problem is painless composition in time using `bind`. We do not want to end up in a nested function mess like this:

```python
hello_world = bind(button("Show Another Button"),
    lambda _: bind(button("Another Button"),
        lambda _: text("Clicked Another Button!")
        )
    )
```

We need to have syntax sugar for composition in time, similarly to Purescript. Luckily, Python synchronous generators compose monadically, the same way our Widgets do, and provide a rather nice notation. We can implement Widgets as generators, and get the nice syntax for free:

```python
def hello_world():
    yield from button("Show Another Button")
    yield

    yield from button("Another Button")
    yield

    yield from text("Clicked Another Button!")
```

The `yield` statements are a wart, caused by inflexibility of Python generators. There are other issues I couldn't work around, but they are mostly cosmetic too:

* There are two different variants of `alt`: one composes better, the other one is nicer to use.
* Synchronous generators are used, because Python's asynchronous generators don't compose monadically. Asynchronicity must be handled by the user, whereas in other Concur variants, it is for free.

Here is the counter application written in Python Concur:

```python
import concur as c

def counter_widget():
    counter = 0
    while True:
        action, _ = yield from c.orr([
            c.text(f"Count: {counter}"),
            c.button("Increment"),
            c.button("Decrement"),
            ])
        if action == "Increment":
            counter += 1
        elif action == "Decrement":
            counter -= 1
        yield


if __name__ == "__main__":
    c.main("Counter", counter_widget(), 500, 500)
```

Composition in time is achieved by the loop and the `yield from` generator syntax. Composition in space is achieved by the `c.orr` function, which is (conceptually) just a repeated application of `alt` over the list of widgets.

Using tagged unions and `map` in Python is syntactically heavy, so I opted to have widgets automatically tag their values with the name of the widget. Therefore, a `c.button("Increment")` returns a tuple `("Increment", None)`, which is pattern-matched by the `if-elif` block below.

# Does it Scale?

We saw how Concur works in toy examples. But does the paradigm also work for real-world complex applications? The answer is simple: yes. And the proof is simple, too. Turns out that you can implement well-known and industry-proven architectures in a few lines of Concur. Concur subsumes [The Elm Architecture](https://guide.elm-lang.org/architecture/) and [Redux](https://redux.js.org/). That's what you get when you choose good, minimal abstractions for the problem at hand.

Redux is five lines in Concur JS:

```js
function redux(state, render, update) {
  let action = yield* render(state)
  let newState = update(state, action)
  yield* redux(newState, render, update)
}
```

The Elm Architecture is three lines in Purescript Concur:
```haskell
tea :: ∀ a s m x. Monad m => s -> (s -> m a) -> (a -> s -> s) -> m x
tea s render update = go s where
    go st = render st >>= (flip update st >>> go)
```

This function is more of a curiosity, because you can use The Elm Architecture directly, without any glue code whatsoever.

Using the Elm architecture is the most obvious way to program in Concur. It looks something like this:

1. **View**: You create a widget tree from application state using spatial composition. The simple event types of widgets are transformed into one big event type, which represents all the events your component or application supports. This is forced by the nature of Concur, as it insists on spatially composing only widgets with the same event type.
2. **Update**: These events are passed by the temporal composition primitives into an update "widget", which takes the old application state and an event, and produces new application state.
3. The new application state is passed recursively, or by a loop, back into **View**.

You can create multiple independent View-Update loops in your application, effectively separating different components at arbitrary granularity. This naturally leads to flexible and clean design, even in complex applications.


# Why hasn't it been done before?

* Object-oriented mindset insists on weaving together state & behavior. This prevents sufficient simplification.
* Mainstream programming languages lack sum types, which are crucial for events. Dynamic type systems are also OK, but that is fairly non-obvious.
* Virtual DOM or ImGui are needed for implementation. They haven't become mainstream until recently.

Also, to an extent, it has been done before. The Elm Architecture and React+Redux seem to be subsets of Concur, and their programming style is similar.


# Conclusion

 We identified the simplest atomic constructs which are still sufficient for UI creation. In doing so, we arrived at a surprisingly simple, yet powerful abstraction around widget composition. This abstraction allows us to be simultaneously simpler and more powerful than well-known libraries, such as React/Redux and Elm. And **way** simpler than MVC event-driven UI libraries.

 To make composition more pleasant to work with, language constructs such as generator syntax, or do-notation are used. This works in a range of different languages, as demonstrated by the multiple variations of the Concur library.

 For more thorough documentation & usage examples, see the project pages of concrete Concur variants. [Purescript Concur](https://github.com/ajnsit/purescript-concur) and [Python Concur](https://github.com/potocpav/python-concur) are the most actively maintained ones at the moment.

# &nbsp;

[^type_syntax]: `Widget a` in Haskell would be `Widget<T>` in C++.
[^function_syntax]: The `a :: b` notation signifies that `a` has the type of `b`. Functions with multiple arguments are notated as `f :: a -> b -> c -> ...`, where the type after the last arrow is the return type.
[^join]: We first `map` both widgets to the same type `Widget (Either a b)`, then we compose them with `alt`. In Purescript, it could be written as `join a b = alt (map Left a) (map Right b)`.
[^nesting]: I haven't mentioned widgets nested in other widgets. This is not a thing we will abstract, because there are multiple possibilities of how things can be nested. If a widget contains other widgets, it will take them as arguments during construction.
[^widget_type]: The actual type is a bit more complicated: `Widget HTML T`. We can ignore `HTML`, as it just enables using multiple back-ends.
[^conceptually]: Conceptually, but that would be a bit slow. The list is actually merged inside a single function.
[^bind]: After syntax sugar expansion, the code is `bind (D.div' [...]) (\n -> counterWidget n)`, where `\n -> ...` is a lambda function.
