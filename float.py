Authors: Luke Matzner, Lauren Sdun, Julia Baumgarten

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

    def _coerce(self, other: NumberLike) -> "HighPrecisionFloat":
        return other if isinstance(other, HighPrecisionFloat) else HighPrecisionFloat(other, bits=self.bits)

    def __add__(self, other: NumberLike) -> "HighPrecisionFloat":
        other = self._coerce(other)
        return HighPrecisionFloat(self.value + other.value, bits=max(self.bits, other.bits))

