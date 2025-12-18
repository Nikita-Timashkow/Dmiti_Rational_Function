from N.Natural import Natural
from Z.Integer import Integer
from Q.Rational import Rational
from TRANS.TRANS_N_Z import TRANS_N_Z



class Polynomial:
    def __init__(self, m, C):
        self.m = m  # int степень многочлена
        self.C = C  # [] массив коэффициентов из Rational

    def ZER_P_B(self):
        """Проверка, является ли полином нулевым"""
        return all(coeff.numerator.A == [0] for coeff in self.C)

    def __add__(self, other):
        """
        Богданов Никита Константинович
        Сложение многочленов
        """

        max_degree = max(self.m, other.m)

        # Создаем массив для коэффициентов результата (от старшей степени к младшей)
        result_coeffs = []

        for i in range(max_degree + 1):

            degree = max_degree - i  # Текущая степень (от старшей к младшей)

            # Находим соответствующие коэффициенты
            self_index = self.m - degree if degree <= self.m else -1
            other_index = other.m - degree if degree <= other.m else -1

            if self_index >= 0 and self_index <= self.m:
                coeff1 = self.C[self_index]
            else:
                coeff1 = Rational(Integer(0, 0, [0]), Natural(0, [1]))

            if other_index >= 0 and other_index <= other.m:
                coeff2 = other.C[other_index]
            else:
                coeff2 = Rational(Integer(0, 0, [0]), Natural(0, [1]))

            # Складываем коэффициенты используя метод ADD_QQ_Q
            sum_coeff = coeff1 + coeff2
            result_coeffs.append(sum_coeff)

        # Убираем ведущие нули (в начале массива)
        while len(result_coeffs) > 1 and result_coeffs[0].numerator.A == [0]:
            result_coeffs.pop(0)
            max_degree -= 1

        result_degree = len(result_coeffs) - 1

        return Polynomial(result_degree, result_coeffs)

    def __sub__(self, other):
        """
        Богданов Никита Константинович
        Вычитание многочленов
        """

        max_degree = max(self.m, other.m)

        # Создаем массив для коэффициентов результата (от старшей степени к младшей)
        result_coeffs = []

        for i in range(max_degree + 1):

            degree = max_degree - i  # Текущая степень (от старшей к младшей)

            # Находим соответствующие коэффициенты
            self_index = self.m - degree if degree <= self.m else -1
            other_index = other.m - degree if degree <= other.m else -1

            if self_index >= 0 and self_index <= self.m:
                coeff1 = self.C[self_index]
            else:
                coeff1 = Rational(Integer(0, 0, [0]), Natural(0, [1]))

            if other_index >= 0 and other_index <= other.m:
                coeff2 = other.C[other_index]
            else:
                coeff2 = Rational(Integer(0, 0, [0]), Natural(0, [1]))

            # Вычитаем коэффициенты используя метод SUB_QQ_Q
            diff_coeff = coeff1-coeff2
            result_coeffs.append(diff_coeff)

        # Убираем ведущие нули (в начале массива)
        while len(result_coeffs) > 1 and result_coeffs[0].numerator.A == [0]:
            result_coeffs.pop(0)
            max_degree -= 1

        result_degree = len(result_coeffs) - 1

        return Polynomial(result_degree, result_coeffs)

    def MUL_PQ_P(self, q: Rational):
        """
        Сделал: Захаренко Александр
        Умножение многочлена на рациональное число
        """

        new_C = []  # массив для новых коэффициентов
        for i in range(len(self.C)):  # Проходимся по коэффициентам (Rational)
            if self.C[i].numerator.A == 0:
                tmp = self.C[i]
            else:
                tmp = self.C[i] * q # Умножаем их на заданное число q
            new_C.append(tmp.RED_Q_Q())  # Cокращаем дробь и добавляем в массив коэффициентов

        return Polynomial(self.m, new_C)  # Формируем новый полином

    def MUL_Pxk_P(self, k: int):
        """
        Сделал: Захаренко Александр
        Умножение многочлена на x^k,
        k - натуральное или 0
        """

        new_m = self.m + k  # новая степень полинома

        # добавляем k нулевых дробей в исходный массив коэффициентов
        new_C = self.C + ([Rational(Integer(0, 1, [0]), Natural(1, [1]))] * k)

        return Polynomial(new_m, new_C)  # Возвращаем новый полином

    def LED_P_Q(self):
        """
        Выполнил: Сурин Максим
        Возвращает старший коэффициент многочлена
        """

        """ Проверка на пустой многочлен """
        if not self.C or self.m < 0:
            return Rational(Integer(0, 0, [0]), Natural(0, [1]))

        return self.C[0]  # Старший коэффициент - первый в массиве

    def DEG_P_N(self):
        """
        Сделал: Чумаков Никита Ярославович
        DEG_P_N: Polynomial → Natural
        Возвращает степень многочлена как натуральное число.
        """
        # Получаем степень многочлена (int)
        m = self.m

        # Преобразуем в массив цифр
        A = [int(d) for d in str(m)]

        # Создаём объект Natural
        N = Natural(len(A) - 1, A)

        return N

    def __mul__(self, other):
        """
        Выполнил: Сурин Максим
        Умножение многочленов
        """

        """ Инициализация нулевого полинома """
        product = Polynomial(0, [Rational(Integer(0, 0, [0]), Natural(0, [1]))])

        """ 
        Умножение длинного полинома на каждый член короткого полинома:
        1) умножение на коэффициент каждого члена 
        2) домножение на x^(степень текущего члена), если его коэффициент не ноль
        """
        if self.m <= other.m:
            shorter, longer = self, other
        else:
            shorter, longer = other, self

        for i in range(shorter.m + 1):
            temp_poly = longer.MUL_PQ_P(shorter.C[i])
            if shorter.C[i].numerator.A != [0]:
                temp_poly = temp_poly.MUL_Pxk_P(shorter.m - i)

            product = product + temp_poly

        return product

    def __floordiv__(self, other):
        """
        делал: Чумаков Никита Ярославович
        Частное от деления многочлена P1 на P2 при делении с остатком.
        """
        # Проверка делителя на нуль
        if all(d.numerator.A == [0] for d in other.C):
            raise ZeroDivisionError("Деление на нулевой многочлен невозможно")

        # Копии делимого и делителя
        A = Polynomial(self.m, self.C[:])
        B = Polynomial(other.m, other.C[:])

        # Частное Q = 0
        zero_rat = Rational(Integer(0, 0, [0]), Natural(0, [1]))
        Q = Polynomial(0, [zero_rat])

        # Основной цикл деления
        while True:
            # Вычисляем степени
            degA = A.m
            degB = B.m

            # Если степень делимого меньше или делимое == 0 — заканчиваем
            if degA < degB or all(c.numerator.A == [0] for c in A.C):
                break

            # Разность степеней
            k = degA - degB

            # Старшие коэффициенты (C[0] — старший)
            a_lead = A.C[0]
            b_lead = B.C[0]

            # Делим коэффициенты (Rational)
            factor = a_lead / b_lead

            # Создаём одночлен factor * x^k
            term = Polynomial(0, [factor])
            term_shifted = term.MUL_Pxk_P(k)

            # Прибавляем одночлен к частному (будущий ответ)
            Q = Q.__add__(term_shifted)  # Используем __add__ вместо +

            # Умножаем делитель на factor и x^k
            B_shifted = B.MUL_Pxk_P(k)  # умножаем на x^k
            B_scaled_coeffs = []
            for c in B_shifted.C:
                B_scaled_coeffs.append(c * factor)  # Умножаем все коэф. делителя на factor
            B_scaled = Polynomial(B_shifted.m, B_scaled_coeffs)

            # Вычитаем (A = A - B_scaled)
            A = A - B_scaled

            # Удаляем ведущие нули, если появились
            while len(A.C) > 1 and A.C[0].numerator.A == [0]:
                A.C.pop(0)
                A.m -= 1

        # Корректируем степень частного (удаляем ведущие нули)
        while len(Q.C) > 1 and Q.C[0].numerator.A == [0]:
            Q.C.pop(0)
        Q.m = len(Q.C) - 1

        return Q

    def __mod__(self, other):
        """
        Сделала: Имховик Наталья
        Нахождение остатка от деления многочлена на
        многочлен при делении с остатком
        Возвращает многочлен
        """
        # Находим частное от деления многочленов
        quotient = self // other

        # Находим произведение частного и делителя
        product = quotient * other

        # Остаток от деления равен разности делимого и полученного произведения
        return self - product

    def GCF_PP_P(self, other):
        """
        Сделала: Имховик Наталья
        Нахождение НОД многочленов
        Используется алгоритм Евклида,
        полученный многочлен нормализуется
        Возвращает многочлен
        """
        # Копируем исходные многочлены
        A = Polynomial(self.m, self.C[:])
        B = Polynomial(other.m, other.C[:])

        # Алгоритм Евклида нахождения НОД
        while not all(c.numerator.A == [0] for c in B.C):
            # B - многочлен с меньшей степенью
            if A.m < B.m:
                A, B = B, A
            R = A % B
            A, B = B, R

        # Нормализация: старший коэффициент равен 1
        if not all(c.numerator.A == [0] for c in A.C):
            normalizer = Rational(Integer(0, 0, [1]), Natural(0, [1])) / A.LED_P_Q()
            A = A.MUL_PQ_P(normalizer)

        return A

    def DER_P_P(self):
        """Сделал: Соколовский Артём - производная многочлена"""
        if self.m == 0:
            zero = Rational(Integer(0, 0, [0]), Natural(0, [1]))
            return Polynomial(0, [zero])

        coeffs = []
        for i in range(self.m):
            # Для степени self.m - i, производная будет (self.m - i) * коэффициент
            power = self.m - i
            r = self.C[i]

            # Создаем натуральное число для степени
            if power < 10:
                k_nat = Natural(0, [power])
            else:
                k_digits = [int(d) for d in str(power)]
                k_nat = Natural(len(k_digits) - 1, k_digits)

            # Преобразуем в целое число
            k_int = TRANS_N_Z(k_nat)

            # Умножаем коэффициент на степень
            new_num = r.numerator * k_int
            coeffs.append(Rational(new_num, Natural(r.denominator.len, r.denominator.A[:])))

        return Polynomial(self.m - 1, coeffs)

    def FAC_P_Q(self):
        """
        Вынесение из многочлена максимального общего числового множителя.
        Ищет ОБЩИЙ множитель для ВСЕХ коэффициентов.
        """

        if self.m < 0 or all(c.numerator.A == [0] for c in self.C):
            one = Rational(Integer(0, 0, [1]), Natural(0, [1]))
            zero = Rational(Integer(0, 0, [0]), Natural(0, [1]))
            return one, Polynomial(0, [zero])

        # Ищем НАИБОЛЬШИЙ общий делитель всех коэффициентов как дробей
        # Общий множитель = НОД(числителей) / НОК(знаменателей)

        # Сначала приводим все коэффициенты к общему знаменателю
        # 1. Находим НОК всех знаменателей
        lcm_den = Natural(0, [1])  # 1
        self.C = [coeff.RED_Q_Q() for coeff in self.C]
        for coeff in self.C:
            if coeff.numerator.A != [0]:
                lcm_den = lcm_den.LCM_NN_N(coeff.denominator)

        # 2. Приводим все коэффициенты к знаменателю lcm_den
        # и собираем числители
        numerators = []
        for coeff in self.C:
            if coeff.numerator.A == [0]:
                numerators.append(Natural(0, [0]))  # 0
            else:
                # Приводим к общему знаменателю: coeff * (lcm_den/denom)
                # Но нам нужен только числитель
                multiplier = lcm_den // coeff.denominator
                # Умножаем числитель на multiplier
                abs_num = coeff.numerator.ABS_Z_Z()
                num_nat = Natural(abs_num.len, abs_num.A[:])
                multiplied_num = num_nat * multiplier

                # Учитываем знак
                if coeff.numerator.s == 1:  # отрицательный
                    # Пока храним как натуральное, знак учтем позже
                    numerators.append(multiplied_num)
                else:
                    numerators.append(multiplied_num)

        # 3. Находим НОД всех этих числителей
        gcd_numerators = None
        for num in numerators:
            if num.A != [0]:  # не нулевой
                if gcd_numerators is None:
                    gcd_numerators = num
                else:
                    gcd_numerators = gcd_numerators.GCF_NN_N(num)

        if gcd_numerators is None:
            gcd_numerators = Natural(0, [1])  # 1

        # 4. Проверяем, что gcd_numerators делится на lcm_den
        # Если да, то можем вынести gcd_numerators/lcm_den
        # Иначе выносим gcd_num/lcm_den где gcd_num = НОД(исходных числителей)

        # Вариант A: gcd_numerators делится на lcm_den
        # Заменяем целочисленное деление на проверку делимости
        if (gcd_numerators % lcm_den).A == [0]:  # Делится нацело
            factor_numerator = gcd_numerators // lcm_den
            factor_denominator = Natural(0, [1])
        else:
            # Вариант B: ищем общий делитель исходных коэффициентов
            gcd_orig = None
            for coeff in self.C:
                if coeff.numerator.A != [0]:
                    abs_num = coeff.numerator.ABS_Z_Z()
                    num_nat = Natural(abs_num.len, abs_num.A[:])
                    if gcd_orig is None:
                        gcd_orig = num_nat
                    else:
                        gcd_orig = gcd_orig.GCF_NN_N(num_nat)

            if gcd_orig is None:
                gcd_orig = Natural(0, [1])

            factor_numerator = gcd_orig
            factor_denominator = lcm_den

        # 5. Создаем множитель
        gcd_int = Integer(0, factor_numerator.len, factor_numerator.A[:])
        factor = Rational(gcd_int, factor_denominator)

        # 6. Упрощаем полином
        new_coeffs = []
        for coeff in self.C:
            if coeff.numerator.A == [0]:
                new_coeffs.append(Rational(Integer(0, 0, [0]), Natural(0, [1])))
            else:
                # Делим коэффициент на множитель
                new_coeff = coeff / factor
                new_coeffs.append(new_coeff.RED_Q_Q())

        # Убираем ведущие нули
        while len(new_coeffs) > 1 and new_coeffs[0].numerator.A == [0]:
            new_coeffs.pop(0)

        new_degree = len(new_coeffs) - 1

        return factor, Polynomial(new_degree, new_coeffs)

    def NMR_P_P(self):
        """Сделал: Соколовский Артём - неприводимый многочлен"""
        dp = self.DER_P_P()
        g = self.GCF_PP_P(dp)
        return self // g

    def show(self):
        p = self
        s = ''

        if p.C[0].numerator.A[0] == 0:
            return '0'

        first = True
        for i in range(p.m + 1):
            coeff = p.C[i]

            if coeff.numerator.A[0] == 0:
                continue

            degree = p.m - i

            # ОБРАБОТКА ЗНАКА (ИСПРАВЛЕНО!)
            if not first:
                if coeff.numerator.s == 0:
                    s += ' + '
                else:
                    s += ' - '
            else:
                first = False
                if coeff.numerator.s == 1:
                    s += '-'

            coeff_str = coeff.show()
            # Убираем минус если он есть в начале
            if coeff_str.startswith('-'):
                coeff_str = coeff_str[1:]

            # ТЕПЕРЬ ПРАВИЛЬНО ОБРАБАТЫВАЕМ 1 И -1
            if degree == 0:
                s += coeff_str
            else:
                if coeff_str == '1':
                    if degree == 1:
                        s += 'x'
                    else:
                        s += f'x^{degree}'
                else:
                    if degree == 1:
                        s += f'{coeff_str}x'
                    else:
                        s += f'{coeff_str}x^{degree}'

        return s