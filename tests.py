import unittest
from typing import Callable, ParamSpec

from paramorator import paramorator

P = ParamSpec("P")


@paramorator
def multiply(func: Callable[P, float], factor: float = 2) -> Callable[P, float]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> float:
        return factor * func(*args, **kwargs)

    return wrapper


class Tests(unittest.TestCase):
    def test_decorator_usage(self):
        @multiply(factor=3)
        def add_then_triple(a: float, b: float) -> float:
            return a + b

        self.assertEqual(add_then_triple(2, 3), 15)

    def test_inline_usage(self):
        sub_then_double = multiply(lambda a, b: a - b, factor=2)
        self.assertEqual(sub_then_double(5, 3), 4)


if __name__ == "__main__":
    unittest.main()
