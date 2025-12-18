# TRANS_STR_RF.py
from P.Polynomial import Polynomial
from Q.Rational import Rational
from Z.Integer import Integer
from N.Natural import Natural
from TRANS.TRANS_STR_P import TRANS_STR_P
from R_F.RationalFunction import RationalFunction


def TRANS_STR_RF(s: str) -> RationalFunction:
    """
    Преобразование строки в рациональную функцию

    Форматы:
    - "полином/полином"
    - "полином" (знаменатель = 1)
    """
    s = s.strip()

    if '/' in s:
        # Разделяем на числитель и знаменатель
        parts = s.split('/')
        if len(parts) != 2:
            raise ValueError(f"Неправильный формат дроби: {s}")

        num_str = parts[0].strip(' ()')
        denom_str = parts[1].strip(' ()')

        # Парсим полиномы
        numerator = TRANS_STR_P(num_str) if num_str else Polynomial(0, [Rational(Integer(0, 0, [0]), Natural(0, [1]))])
        denominator = TRANS_STR_P(denom_str) if denom_str else Polynomial(0, [
            Rational(Integer(0, 0, [1]), Natural(0, [1]))])

        return RationalFunction(numerator, denominator)
    else:
        # Просто полином
        numerator = TRANS_STR_P(s)
        # Знаменатель = 1
        one_rat = Rational(Integer(0, 0, [1]), Natural(0, [1]))
        denominator = Polynomial(0, [one_rat])

        return RationalFunction(numerator, denominator)