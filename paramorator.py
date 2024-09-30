"""A dead simple utility for defining decorators with parameters that make type checkers happy."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Concatenate, ParamSpec, TypeVar, Protocol, overload

    C_contra = TypeVar("C_contra", bound=Callable, contravariant=True)
    C = TypeVar("C", bound=Callable)
    D_co = TypeVar("D_co", bound=Callable, covariant=True)
    D = TypeVar("D", bound=Callable)
    P = ParamSpec("P")

    class Decorator(Protocol[C_contra, P, D_co]):
        """An optionally parameterized decorator protocol."""

        @overload
        def __call__(
            self, func: None = ..., /, *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[C_contra], D_co]: ...

        @overload
        def __call__(
            self, func: C_contra, /, *args: P.args, **kwargs: P.kwargs
        ) -> D_co: ...

        def __call__(
            self, func: C_contra | None = ..., /, *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[C_contra], D_co] | D_co: ...


__version__ = "1.0.1"


def paramorator(deco: Callable[Concatenate[C, P], D]) -> Decorator[C, P, D]:
    """A decorator for defining type-checked decorators with parameters.

    ```python
    from typing import Callable, ParamSpec

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

    sub_then_double = multiply(lambda a, b: a - b, factor=2)
    assert sub_then_double(5, 3) == 4
    ```

    Args:
        deco: A decorator function that accepts a callable and additional parameters.

    Returns:
        A decorator that can be parameterized with keyword arguments.
    """

    if TYPE_CHECKING:

        @overload
        def wrapper(
            func: None = ..., /, *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[C], D]: ...

        @overload
        def wrapper(func: C, /, *args: P.args, **kwargs: P.kwargs) -> D: ...

    @wraps(deco)
    def wrapper(
        func: C | None = None, /, *args: P.args, **kwargs: P.kwargs
    ) -> Callable[[C], D] | D:
        if func is None:
            return lambda func: deco(func, *args, **kwargs)
        else:
            return deco(func, *args, **kwargs)

    return wrapper
