# Authors: Luke Matzner, Lauren Sdun, Julia Baumgarten

from decimal import Decimal, localcontext
from typing import Union, Any
from contextlib import contextmanager

NumberLike = Union[int, float, str, "HighPrecisionFloat"]

def bits_to_decimal_digits(bits: int) -> int:
    """Digits approximately bits * log10(2) approximately bits * 0.30103 and subtract 1 for safety"""
    return max(1, int(bits * 0.30102999566) - 1)

class HighPrecisionFloat:
    """High-precision float backed by Decimal +, -, *, /"""
    __slots__ = ("value", "bits")

    def __init__(self, x: NumberLike, bits: int = 128):
        self.bits = int(bits)
        with localcontext() as ctx:
            ctx.prec = bits_to_decimal_digits(self.bits)
            if isinstance(x, HighPrecisionFloat):
                self.value = Decimal(x.value)
            else:
                self.value = Decimal(str(x))

    @contextmanager
    def _ctx(self, other: Any = None):
        use_bits = self.bits if not isinstance(other, HighPrecisionFloat) else max(self.bits, other.bits)
        with localcontext() as ctx:
            ctx.prec = bits_to_decimal_digits(use_bits)
            yield

    def _coerce(self, other: NumberLike) -> "HighPrecisionFloat":
        return other if isinstance(other, HighPrecisionFloat) else HighPrecisionFloat(other, bits=self.bits)

    def __add__(self, other: NumberLike) -> "HighPrecisionFloat":
        other = self._coerce(other)
        with self._ctx(other):
            return HighPrecisionFloat(self.value + other.value, bits=max(self.bits, other.bits))

    def __sub__(self, other: NumberLike) -> "HighPrecisionFloat":
        other = self._coerce(other)
        with self._ctx(other):
            return HighPrecisionFloat(self.value - other.value, bits=max(self.bits, other.bits))

    def __mul__(self, other: NumberLike) -> "HighPrecisionFloat":
        other = self._coerce(other)
        with self._ctx(other):
            return HighPrecisionFloat(self.value * other.value, bits=max(self.bits, other.bits))

    def __truediv__(self, other: NumberLike) -> "HighPrecisionFloat":
        other = self._coerce(other)
        if other.value == 0:
            raise ZeroDivisionError("error")
        with self._ctx(other):
            return HighPrecisionFloat(self.value / other.value, bits=max(self.bits, other.bits))

    def __gt__(self, other: NumberLike) -> bool:
        other = self._coerce(other)
        with self._ctx(other):
            if self.value > other.value: return True
            else: return False
    
    def __lt__(self,other: NumberLike) -> bool:
        other = self._coerce(other)
        with self._ctx(other):
            if self.value < other.value: return True
            else: return False

    def __lt__(self, other): return self._cmp(other) < 0

    def __str__(self) -> str:
        return str(self.value)

# Testing the addition function:
a = HighPrecisionFloat(1234567890.09876543210987654321, bits=256)
b = HighPrecisionFloat(9876543210.01234567890987654321, bits=256)
c = a + b
print(f"a + b = {c}")

# Testing the subtraction function:
f = a - b
print(f"a - b = {f}")

# Testing the multiplication function:
g = a * b
print(f"a * b = {g}")

# Testing the division function:
h = a / b
print(f"a / b = {h}")
