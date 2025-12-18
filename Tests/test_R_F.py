from R_F.RationalFunction import *
import unittest


class TestRationalFunction(unittest.TestCase):
    """Юнит-тесты для RationalFunction"""

    # Вспомогательные методы как обычные методы класса
    def create_rational(self, n):
        """Создает Rational из целого числа"""
        sign = 1 if n < 0 else 0
        digits = [int(d) for d in str(abs(n))]
        return Rational(Integer(sign, len(digits) - 1, digits), Natural(0, [1]))

    def create_poly(self, coeffs):
        """Создает Polynomial из списка коэффициентов"""
        rationals = [self.create_rational(c) for c in coeffs]
        return Polynomial(len(rationals) - 1, rationals)

    def create_rf(self, num_coeffs, den_coeffs):
        """Создает RationalFunction из списков коэффициентов"""
        return RationalFunction(
            self.create_poly(num_coeffs),
            self.create_poly(den_coeffs)
        )

    # ------------------------------------------------------------
    # ТЕСТЫ НА БАЗОВОЕ СОКРАЩЕНИЕ
    # ------------------------------------------------------------

    def test_basic_reduction(self):
        """Тест базового сокращения дробей"""
        # (-x² + 4)/(x - 2) = -x - 2
        rf = self.create_rf([-1, 0, 4], [1, -2])
        self.assertEqual(rf.show(), "-x - 2")
        self.assertTrue(rf.is_polynomial())

    def test_simple_fraction(self):
        """Тест простой дроби"""
        # (x² - 4)/(x + 2) = x - 2
        rf = self.create_rf([1, 0, -4], [1, 2])
        self.assertEqual(rf.show(), "x - 2")

    def test_fraction_to_one(self):
        """Тест сокращения до 1"""
        # (x+1)/(x+1) = 1
        rf = self.create_rf([1, 1], [1, 1])
        self.assertEqual(rf.show(), "1")
        self.assertTrue(rf.is_polynomial())

    # ------------------------------------------------------------
    # ТЕСТЫ НА СЛОЖЕНИЕ/ВЫЧИТАНИЕ
    # ------------------------------------------------------------

    def test_addition_same_denominator(self):
        """Тест сложения с одинаковым знаменателем"""
        # (x+1)/(x+2) + (x+3)/(x+2) = (2x+4)/(x+2) = 2
        rf1 = self.create_rf([1, 1], [1, 2])
        rf2 = self.create_rf([1, 3], [1, 2])
        result = rf1 + rf2
        self.assertEqual(result.show(), "2")

    def test_addition_different_denominators(self):
        """Тест сложения с разными знаменателями"""
        # 1/(x+1) + 1/(x-1) = 2x/(x²-1)
        rf1 = self.create_rf([1], [1, 1])
        rf2 = self.create_rf([1], [1, -1])
        result = rf1 + rf2
        self.assertEqual(result.show(), "(2x)/(x^2 - 1)")

    def test_subtraction(self):
        """Тест вычитания"""
        # (x+2)/(x+3) - (x+1)/(x+2)
        rf1 = self.create_rf([1, 2], [1, 3])
        rf2 = self.create_rf([1, 1], [1, 2])
        result = rf1 - rf2
        # Проверяем что результат не нулевой
        self.assertNotEqual(result.show(), "0")

    # ------------------------------------------------------------
    # ТЕСТЫ НА УМНОЖЕНИЕ/ДЕЛЕНИЕ
    # ------------------------------------------------------------

    def test_multiplication_cancellation(self):
        """Тест умножения с сокращением"""
        # (x+1)/(x+2) * (x+2)/(x+3) = (x+1)/(x+3)
        rf1 = self.create_rf([1, 1], [1, 2])
        rf2 = self.create_rf([1, 2], [1, 3])
        result = rf1 * rf2
        self.assertEqual(result.show(), "(x + 1)/(x + 3)")

    def test_division(self):
        """Тест деления"""
        # (x²-4)/(x+1) ÷ (x+2)/(x-1)
        rf1 = self.create_rf([1, 0, -4], [1, 1])
        rf2 = self.create_rf([1, 2], [1, -1])
        result = rf1 / rf2
        # Проверяем что в числителе есть x²
        self.assertIn("x^2", result.numerator.show())

    def test_multiplication_inverse(self):
        """Тест умножения взаимно обратных дробей"""
        # (x+2)/(x+3) * (x+3)/(x+2) = 1
        rf1 = self.create_rf([1, 2], [1, 3])
        rf2 = self.create_rf([1, 3], [1, 2])
        result = rf1 * rf2
        self.assertEqual(result.show(), "1")

    # ------------------------------------------------------------
    # ТЕСТЫ НА ВЫСОКИЕ СТЕПЕНИ
    # ------------------------------------------------------------

    def test_high_degree_power_difference(self):
        """Тест разности степеней"""
        # (x^10 - 1)/(x^5 - 1) = x^5 + 1
        num = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]  # x^10 - 1
        den = [1, 0, 0, 0, 0, -1]  # x^5 - 1
        num_poly = self.create_poly(num)
        den_poly = self.create_poly(den)
        rf = RationalFunction(num_poly, den_poly)

        result = rf.show()
        self.assertEqual(result, "x^5 + 1")

    # ------------------------------------------------------------
    # ТЕСТЫ НА НУЛИ И ГРАНИЧНЫЕ СЛУЧАИ
    # ------------------------------------------------------------

    def test_zero_function(self):
        """Тест нулевой функции"""
        # 0/1 = 0
        rf = self.create_rf([0], [1])
        self.assertEqual(rf.show(), "0")
        self.assertTrue(rf.is_polynomial())

    def test_addition_with_zero(self):
        """Тест сложения с нулем"""
        # 0 + (x+1)/(x+2) = (x+1)/(x+2)
        zero = self.create_rf([0], [1])
        rf = self.create_rf([1, 1], [1, 2])
        result = zero + rf
        self.assertEqual(result.show(), "(x + 1)/(x + 2)")

    def test_multiplication_by_zero(self):
        """Тест умножения на ноль"""
        # 0 * любая_дробь = 0
        zero = self.create_rf([0], [1])
        rf = self.create_rf([1, 2, 3], [1, 4, 5])
        result = zero * rf
        self.assertEqual(result.show(), "0")

    # ------------------------------------------------------------
    # ТЕСТЫ НА ЗНАКИ
    # ------------------------------------------------------------

    def test_negative_coefficients(self):
        """Тест отрицательных коэффициентов"""
        # (-x² + 4)/(x - 2) = -x - 2
        rf = self.create_rf([-1, 0, 4], [1, -2])
        self.assertEqual(rf.show(), "-x - 2")

    def test_all_negative_fraction(self):
        """Тест дроби со всеми отрицательными коэффициентами"""
        # (-2x² - 3x - 1)/(-x - 2)
        rf = self.create_rf([-2, -3, -1], [-1, -2])
        # Просто проверяем что работает без ошибок
        self.assertEqual(rf.show(), "(2x^2 + 3x + 1)/(x + 2)")

    # ------------------------------------------------------------
    # ТЕСТЫ НА СЛОЖНЫЕ ВЫРАЖЕНИЯ
    # ------------------------------------------------------------

    def test_complex_expression(self):
        """Тест сложного выражения"""
        A = self.create_rf([1, 1], [1, 2])
        B = self.create_rf([1, 2], [1, 3])
        C = self.create_rf([1, 3], [1, 4])

        result = (A + B) * (C - A) / (B + C)
        # Проверяем что результат не нулевой
        self.assertNotEqual(result.show(), "0")

    def test_chain_operations(self):
        """Тест цепочки операций"""
        # 5 * (x+1)/(x+2)
        base = self.create_rf([1, 1], [1, 2])
        result = base
        for _ in range(4):
            result = result + base

        # Проверяем что результат содержит 5
        self.assertEqual(result.show(), "(5x + 5)/(x + 2)")

    # ------------------------------------------------------------
    # ТЕСТЫ НА ИСКЛЮЧЕНИЯ
    # ------------------------------------------------------------

    def test_division_by_zero_polynomial(self):
        """Тест деления на нулевую функцию"""
        rf1 = self.create_rf([1, 2], [1, 3])
        rf2 = self.create_rf([0], [1])

        # Деление на нулевую функцию должно вызывать исключение
        with self.assertRaises(ZeroDivisionError):
            _ = rf1 / rf2

    def test_constructor_zero_denominator(self):
        """Тест создания функции с нулевым полиномом в знаменателе"""
        # Создаем нулевой полином
        zero_poly = self.create_poly([0])

        # Должно вызывать исключение
        with self.assertRaises(ValueError):
            _ = RationalFunction(self.create_poly([1, 2]), zero_poly)


# Дополнительные тесты производительности
class TestPerformance(unittest.TestCase):
    """Тесты производительности"""

    def setUp(self):
        self.create_rational = lambda n: Rational(
            Integer(1 if n < 0 else 0, len(str(abs(n))) - 1, [int(d) for d in str(abs(n))]),
            Natural(0, [1])
        )

        self.create_poly = lambda coeffs: Polynomial(
            len(coeffs) - 1,
            [self.create_rational(c) for c in coeffs]
        )

    def test_arithmetics_performance(self):
        """Тест производительности арифметических операций"""
        import time

        rf1 = RationalFunction(
            self.create_poly([1, 2, 3, 4, 5, 6]),
            self.create_poly([2, 3, 4, 5, 6, 7])
        )

        rf2 = RationalFunction(
            self.create_poly([2, 3, 4, 5, 6, 7]),
            self.create_poly([1, 2, 3, 4, 5, 6])
        )

        start = time.time()
        result = rf1 + rf2
        end = time.time()

        self.assertIsNotNone(result.show())
        self.assertLess(end - start, 1.0)

        start = time.time()
        result = rf1 * rf2
        end = time.time()

        self.assertIsNotNone(result.show())
        self.assertLess(end - start, 1.0)

        start = time.time()
        result = rf1 / rf2
        end = time.time()
        self.assertIsNotNone(result.show())
        self.assertLess(end - start, 1.0)


# ------------------------------------------------------------
# ТЕСТЫ НА РАЦИОНАЛЬНЫЕ КОЭФФИЦИЕНТЫ
# ------------------------------------------------------------

class TestRationalCoefficients(unittest.TestCase):
    """Тесты для рациональных функций с рациональными коэффициентами"""

    def create_rational_number(self, num, den=1):
        """Создает Rational число из числителя и знаменателя"""
        sign_num = 1 if num < 0 else 0
        sign_den = 1 if den < 0 else 0
        num_digits = [int(d) for d in str(abs(num))]
        den_digits = [int(d) for d in str(abs(den))]

        num_int = Integer(sign_num, len(num_digits) - 1, num_digits)
        den_nat = Natural(len(den_digits) - 1, den_digits)
        return Rational(num_int, den_nat)

    def create_poly_with_rational_coeffs(self, coeffs):
        """Создает полином с рациональными коэффициентами"""
        # coeffs = [(num1, den1), (num2, den2), ...] или ["1/2", "3/4", ...]
        rationals = []
        for coeff in coeffs:
            if isinstance(coeff, str):
                if '/' in coeff:
                    num, den = coeff.split('/')
                    rationals.append(self.create_rational_number(int(num), int(den)))
                else:
                    rationals.append(self.create_rational_number(int(coeff)))
            elif isinstance(coeff, tuple):
                num, den = coeff
                rationals.append(self.create_rational_number(num, den))
            else:
                rationals.append(self.create_rational_number(coeff))
        return Polynomial(len(rationals) - 1, rationals)

    def test_rational_coefficient_simplification(self):
        """Тест упрощения с рациональными коэффициентами"""
        # (5/2) / (5/2) = 1
        num_poly = self.create_poly_with_rational_coeffs([(5, 2)])
        den_poly = self.create_poly_with_rational_coeffs([(5, 2)])
        rf = RationalFunction(num_poly, den_poly)
        self.assertEqual(rf.show(), "1")

    def test_fraction_with_fractional_coefficients(self):
        """Тест дроби с дробными коэффициентами"""
        # (1/2 x² + 2/3 x + 1/4) / (3/4 x + 1/2)
        num_poly = self.create_poly_with_rational_coeffs([(1, 2), (2, 3), (1, 4)])
        den_poly = self.create_poly_with_rational_coeffs([(3, 4), (1, 2)])
        rf = RationalFunction(num_poly, den_poly)

        # Проверяем, что результат содержит дроби
        result = rf.show()
        self.assertIn("/", result)

    def test_addition_rational_coefficients(self):
        """Тест сложения с рациональными коэффициентами"""
        # (1/2)/(x+1) + (1/3)/(x+2)
        rf1 = RationalFunction(
            self.create_poly_with_rational_coeffs([(1, 2)]),
            self.create_poly_with_rational_coeffs([1, 1])
        )
        rf2 = RationalFunction(
            self.create_poly_with_rational_coeffs([(1, 3)]),
            self.create_poly_with_rational_coeffs([1, 2])
        )
        result = rf1 + rf2

        # Результат должен содержать дроби
        self.assertIn("/", result.show())

    def test_multiplication_rational_coefficients(self):
        """Тест умножения с сокращением дробных коэффициентов"""
        # (2/3 x) * (3/2 / x) = 1
        rf1 = RationalFunction(
            self.create_poly_with_rational_coeffs([(2, 3), 0]),  # (2/3)x
            self.create_poly_with_rational_coeffs([1])
        )
        rf2 = RationalFunction(
            self.create_poly_with_rational_coeffs([(3, 2)]),  # 3/2
            self.create_poly_with_rational_coeffs([1, 0])  # x
        )
        result = rf1 * rf2
        self.assertEqual(result.show(), "1")

    def test_division_rational_coefficients(self):
        """Тест деления с дробными коэффициентами"""
        # (4/9 x²) ÷ (2/3 x) = (2/3 x)
        rf1 = RationalFunction(
            self.create_poly_with_rational_coeffs([(4, 9), 0, 0]),  # (4/9)x²
            self.create_poly_with_rational_coeffs([1])
        )
        rf2 = RationalFunction(
            self.create_poly_with_rational_coeffs([(2, 3), 0]),  # (2/3)x
            self.create_poly_with_rational_coeffs([1])
        )
        result = rf1 / rf2
        self.assertIn("2/3", result.show())

    def test_complex_fractional_expression(self):
        """Тест сложного выражения с дробными коэффициентами"""
        # (1/2 x + 1/3) / (3/4 x - 1/5) + (2/5 x + 1/6) / (1/2 x + 2/3)
        rf1 = RationalFunction(
            self.create_poly_with_rational_coeffs([(1, 2), (1, 3)]),
            self.create_poly_with_rational_coeffs([(3, 4), (-1, 5)])
        )
        rf2 = RationalFunction(
            self.create_poly_with_rational_coeffs([(2, 5), (1, 6)]),
            self.create_poly_with_rational_coeffs([(1, 2), (2, 3)])
        )
        result = rf1 + rf2

        # Результат должен быть корректной рациональной функцией
        self.assertIsNotNone(result)
        self.assertTrue(not(result.is_polynomial()))

    def test_numeric_factor_extraction(self):
        """Тест вынесения числовых множителей"""
        # (6/8 x² + 9/12 x + 3/6) = (3/4)(2x² + 3x + 1)
        poly = self.create_poly_with_rational_coeffs([(6, 8), (9, 12), (3, 6)])

        # Создаем рациональную функцию с знаменателем 1
        rf = RationalFunction(poly, self.create_poly_with_rational_coeffs([1]))

        # После нормализации числовой множитель должен быть вынесен
        result = rf.show()
        # Проверяем, что коэффициенты упрощены
        self.assertNotIn("6/8", result)

    def test_rational_coefficient_gcd(self):
        """Тест НОД с рациональными коэффициентами"""
        # (3/4 x² + 3/2 x + 3/4) и (3/2 x + 3/2) имеют НОД (3/2 x + 3/2)
        num_poly = self.create_poly_with_rational_coeffs([(3, 4), (3, 2), (3, 4)])
        den_poly = self.create_poly_with_rational_coeffs([(3, 2), (3, 2)])

        rf = RationalFunction(num_poly, den_poly)
        # После сокращения должен остаться линейный полином
        self.assertEqual(rf.numerator.m, 1)

    def test_mixed_integer_rational_coefficients(self):
        """Тест смешанных целых и дробных коэффициентов"""
        # (2x² + 3/2 x + 1) / (4x + 4/3)
        num_poly = self.create_poly_with_rational_coeffs([2, (3, 2), 1])
        den_poly = self.create_poly_with_rational_coeffs([4, (4, 3)])

        rf = RationalFunction(num_poly, den_poly)
        result = rf.show()

        # Должны быть и целые и дробные коэффициенты
        self.assertEqual(result, "((3/2)x^2 + (9/8)x + (3/4))/(3x + 1)" )

    def test_negative_rational_coefficients(self):
        """Тест отрицательных дробных коэффициентов"""
        # (-1/2 x + 2/3) / (3/4 x - 5/6)
        num_poly = self.create_poly_with_rational_coeffs([(-1, 2), (2, 3)])
        den_poly = self.create_poly_with_rational_coeffs([(3, 4), (-5, 6)])

        rf = RationalFunction(num_poly, den_poly)
        result = rf.show()

        # Проверяем наличие знаков минус в выводе
        self.assertTrue("-" in result or "(-" in result)

    def test_simplify_complex_fraction(self):
        """Тест упрощения сложной дроби с рациональными коэффициентами"""
        # ((1/2 x)/(3/4)) / ((2/3 x)/(5/6))
        numerator = RationalFunction(
            self.create_poly_with_rational_coeffs([(1, 2), 0]),  # (1/2)x
            self.create_poly_with_rational_coeffs([(3, 4)])
        )
        denominator = RationalFunction(
            self.create_poly_with_rational_coeffs([(2, 3), 0]),  # (2/3)x
            self.create_poly_with_rational_coeffs([(5, 6)])
        )
        result = numerator / denominator

        # Результат должен упроститься до константы
        self.assertEqual(result.show(), "(5/6)")

    def test_chain_operations_rational_coeffs(self):
        """Тест цепочки операций с рациональными коэффициентами"""
        A = RationalFunction(
            self.create_poly_with_rational_coeffs([(1, 2), (1, 3)]),
            self.create_poly_with_rational_coeffs([1, (2, 3)])
        )
        B = RationalFunction(
            self.create_poly_with_rational_coeffs([(2, 5), (3, 4)]),
            self.create_poly_with_rational_coeffs([1, (1, 2)])
        )

        # (A + B) * (A - B) / (A * B)
        result = (A + B) * (A - B) / (A * B)

        # Проверяем, что система не падает на сложных выражениях
        self.assertIsNotNone(result.show())

    def test_polynomial_conversion(self):
        """Тест преобразования рациональной функции в полином"""
        # (3/2 x² + 3 x + 3/2) / (3/2) = x² + 2x + 1
        num_poly = self.create_poly_with_rational_coeffs([(3, 2), 3, (3, 2)])
        den_poly = self.create_poly_with_rational_coeffs([(3, 2)])

        rf = RationalFunction(num_poly, den_poly)
        self.assertTrue(rf.is_polynomial())
        # Коэффициенты должны быть целыми после сокращения
        result = rf.show()
        self.assertNotIn("/", result)  # Не должно быть дробей