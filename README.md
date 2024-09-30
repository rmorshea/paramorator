# Paramorator

A dead simple utility for defining decorators with parameters that make type checkers
happy.

## Installation

```bash
pip install paramorator
```

## Usage

```python
from typing import Callable, ParamSpec

from paramorator import paramorator

P = ParamSpec("P")

@paramorator
def multiply(func: Callable[P, float], factor: float = 2) -> Callable[P, float]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> float:
        return factor * func(*args, **kwargs)
    return wrapper


@multiply(factor=3)
def add_then_triple(a: float, b: float) -> float:
    return a + b


assert add_then_triple(2, 3) == 15

# also supports inline usage
sub_then_double = multiply(lambda a, b: a - b, factor=2)
assert sub_then_double(5, 3) == 4
```

This isn't exactly rocket science, but to achieve the same result without `paramorator`,
you need to write a bunch boilerplate code just to satisfy your type checker. Here is
the equivalent `multiple` decorator written without `paramorator`:

```python
from typing import Any, ParamSpec, Callable, overload, cast

P = ParamSpec("P")


@overload
def multiply(func: Callable[P, float], /, factor: float = ...) -> Callable[P, float]:
    ...

@overload
def multiply(func: None = ..., /, factor: float = ...) -> Callable[[Callable[P, float]], Callable[P, float]]:
    ...

def multiply(
    func: Callable[P, float] | None = None,
    /,
    factor: float = 2,
) -> Callable[P, float] | Callable[[Callable[P, float]], Callable[P, float]]:

    def decorator(func: Callable[P, float]) -> Callable[P, float]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> float:
            return factor * func(*args, **kwargs)
        return wrapper

    return decorator(func) if func else decorator
```

## Development

Install [`flit`](https://flit.pypa.io/en/stable/index.html) and run:

```bash
flit install
```

To run tests:

```bash
python tests.py
```

Check the types with Pyright:

```bash
pyright paramorator.py tests.py
```
