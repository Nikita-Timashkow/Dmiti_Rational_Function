from P.Polynomial import Polynomial
from Q.Rational import Rational
from N.Natural import Natural
from Z.Integer import Integer

class RationalFunction:
    """
    Рациональная функция - отношение двух многочленов
    R(x) = P(x) / Q(x), где P и Q - полиномы, Q ≠ 0
    """

    def __init__(self, numerator: Polynomial, denominator: Polynomial):
        """
        Инициализация рациональной функции
        """
        if denominator.ZER_P_B():
            raise ValueError("Знаменатель не может быть нулевым полиномом")

        self.numerator = numerator
        self.denominator = denominator

        # Автоматически сокращаем дробь при создании
        self._normalize()

    def _normalize(self):
        """Сокращение дроби на НОД числителя и знаменателя"""
        # Если числитель нулевой
        if self.numerator.ZER_P_B():
            zero_coeff = Rational(Integer(0, 0, [0]), Natural(0, [1]))
            self.numerator = Polynomial(0, [zero_coeff])
            one_coeff = Rational(Integer(0, 0, [1]), Natural(0, [1]))
            self.denominator = Polynomial(0, [one_coeff])
            return

        # ШАГ 1: Выносим числовые множители через FAC_P_Q
        num_factor, num_simplified = self.numerator.FAC_P_Q()
        den_factor, den_simplified = self.denominator.FAC_P_Q()

        # Общий числовой множитель = НОД(num_factor, den_factor)
        # Сокращаем дробь num_factor/den_factor
        common_numeric_factor = num_factor / den_factor

        # Упрощаем полиномы (уже без числовых множителей)
        self.numerator = num_simplified
        self.denominator = den_simplified

        # ШАГ 2: Находим НОД полиномиальных частей
        gcd_poly = self.numerator.GCF_PP_P(self.denominator)

        # Если НОД не равен 1
        if not self._is_unit_polynomial(gcd_poly):
            # Делим числитель и знаменатель на НОД
            self.numerator = self.numerator // gcd_poly
            self.denominator = self.denominator // gcd_poly
            self._normalize()

        # ШАГ 3: Финальная нормализация
        # Умножаем числитель на сокращенный числовой множитель
        self.numerator = self.numerator.MUL_PQ_P(common_numeric_factor)

        # Нормализация знака знаменателя
        lead_coeff = self.denominator.LED_P_Q()
        if lead_coeff.numerator.s == 1:  # Если отрицательный
            minus_one = Rational(Integer(1, 0, [1]), Natural(0, [1]))  # -1
            self.numerator = self.numerator.MUL_PQ_P(minus_one)
            self.denominator = self.denominator.MUL_PQ_P(minus_one)

    def _is_unit_polynomial(self, poly: Polynomial) -> bool:
        """Проверяет, является ли полином единичным (равен 1)"""
        if poly.m != 0:
            return False
        r = poly.C[0]
        return (r.numerator.A == [1] and
                r.numerator.s == 0 and
                r.denominator.A == [1])

    def __add__(self, other: 'RationalFunction') -> 'RationalFunction':
        """
        Сложение рациональных функций: R1 + R2
        """

        # Получаем числители и общий знаменатель
        (num1, den), (num2, _) = self.common_denominator(other)

        # Складываем числители
        res_num = num1 + num2

        # Создаем результат
        return RationalFunction(res_num, den)

    def __sub__(self, other: 'RationalFunction') -> 'RationalFunction':
        """
        Вычитание рациональных функций: R1 - R2
        """
        (num1, den), (num2, _) = self.common_denominator(other)

        # Вычитаем числители
        res_num = num1 - num2

        return RationalFunction(res_num, den)

    def __mul__(self, other: 'RationalFunction') -> 'RationalFunction':
        """
        Умножение рациональных функций: R1 * R2

        Формула: (P1/Q1) * (P2/Q2) = (P1*P2) / (Q1*Q2)
        """
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator

        return RationalFunction(new_numerator, new_denominator)

    def __truediv__(self, other: 'RationalFunction') -> 'RationalFunction':
        """
        Деление рациональных функций: R1 / R2

        Формула: (P1/Q1) / (P2/Q2) = (P1*Q2) / (Q1*P2)
        """
        # Проверяем, что делитель не нулевой
        if other.numerator.ZER_P_B():
            raise ZeroDivisionError("Деление на нулевой полином")

        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator

        return RationalFunction(new_numerator, new_denominator)

    def common_denominator(self, other: 'RationalFunction') -> [tuple[Polynomial, Polynomial], tuple[Polynomial, Polynomial]]:
        """
        Приведение двух рациональных функций к общему знаменателю
        """
        # Находим НОК знаменателей
        denom1 = self.denominator
        denom2 = other.denominator

        # НОК(P, Q) = P * Q / НОД(P, Q)
        gcd = denom1.GCF_PP_P(denom2)
        lcm = (denom1 * denom2) // gcd

        # Вычисляем дополнительные множители
        factor1 = lcm // denom1
        factor2 = lcm // denom2

        # Приводим к общему знаменателю
        new_num1 = self.numerator * factor1
        new_num2 = other.numerator * factor2

        # Возвращаем числители и общий знаменатель
        return ((new_num1, lcm), (new_num2, lcm))

    def is_polynomial(self) -> bool:
        """Проверка, является ли функция полиномом (знаменатель = 1)"""
        return (self.denominator.m == 0 and
                self.denominator.C[0].numerator.A == [1] and
                self.denominator.C[0].denominator.A == [1])

    def show(self) -> str:
        """Строковое представление рациональной функции"""
        if self.numerator.ZER_P_B():
            return "0"

        num_str = self.numerator.show()
        denom_str = self.denominator.show()

        if self.is_polynomial():
            return num_str

        return f"({num_str})/({denom_str})"

    def __str__(self) -> str:
        return self.show()