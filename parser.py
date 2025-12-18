import re
from P.Polynomial import Polynomial
from Q.Rational import Rational
from TRANS.TRANS_INT_Q import TRANS_INT_Q
from TRANS.TRANS_STR_P import TRANS_STR_P
from TRANS.TRANS_Q_P import TRANS_Q_P
from TRANS.TRANS_INT_N import TRANS_INT_N
from TRANS.TRANS_INT_Z import TRANS_INT_Z
from Z.Integer import Integer
from N.Natural import Natural
from R_F.RationalFunction import RationalFunction


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def to_rpn(expression: str):
    expression = expression.replace(' ', '')

    # Обрабатываем специальные операторы
    expression = expression.replace('//', '§')  # временная замена для целочисленного деления

    # === ДОПОЛНИТЕЛЬНО: вставляем * между скобкой и x ===
    # Например: (...)x → (...)*x
    expression = re.sub(r'(?<=\))(?=x)', '*', expression)
    # Также: число сразу перед x (например 3x) → 3*x
    expression = re.sub(r'(?<=\d)(?=x)', '*', expression)

    # Разбиваем на токены (включая знаки)
    token_pattern = r'(x\^\d+|x|\d+\.\d+|\d+|[+\-*/§%^()])'  # добавлен § и %
    tokens = re.findall(token_pattern, expression)

    # === Обработка унарных минусов ===
    processed = []
    for i, tok in enumerate(tokens):
        if tok == '-':
            # Унарный минус — если стоит в начале или после оператора или открывающей скобки
            if i == 0 or tokens[i - 1] in {'+', '-', '*', '/', '§', '%', '^', '('}:
                if i + 1 < len(tokens):
                    nxt = tokens[i + 1]
                    combined = '-' + nxt
                    processed.append(combined)
                    tokens[i + 1] = ''  # помечаем, что этот токен уже использован
                continue
        if tok != '':
            processed.append(tok)

    # === Алгоритм сортировочной станции ===
    output = []
    stack = []

    precedence = {'^': 4, '*': 3, '/': 3, '§': 3, '%': 3, '+': 2, '-': 2}  # добавлены § и %
    right_assoc = {'^'}

    for token in processed:
        if re.fullmatch(r'-?\d+(\.\d+)?', token) or re.fullmatch(r'-?x(\^\d+)?', token):
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] in precedence:
                top = stack[-1]
                if (token not in right_assoc and precedence[token] <= precedence[top]) or \
                        (token in right_assoc and precedence[token] < precedence[top]):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # убрать '('

    while stack:
        output.append(stack.pop())

    # Заменяем временный символ § обратно на //
    result = []
    for token in output:
        if token == '§':
            result.append('//')
        else:
            result.append(token)

    return result


def eval_rpn_p(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    stack.append(a + b)
                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a + b)
            elif t == '%':
                if type(a) == int or type(b) == int:
                    raise TypeError
                if type(a) == Rational or type(b) == Rational:
                    raise TypeError
                stack.append(a % b)
            elif t == '-':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    stack.append(a - b)
                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a - b)
            elif t == '*':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    stack.append(a * b)
                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a * b)
            elif t == '/':
                if type(a) == int:
                    a = TRANS_INT_Q(a)
                if type(b) == int:
                    b = TRANS_INT_Q(b)
                if type(a) == type(b) and type(a) != str:
                    if type(a) == Polynomial:
                        stack.append(a // b)
                    else:
                        stack.append(a / b)

                else:
                    if type(a) == Rational:
                        a = TRANS_Q_P(a)
                    if type(b) == Rational:
                        b = TRANS_Q_P(b)
                    stack.append(a // b)
            elif t == '^':
                stack.append(a ** b)
        else:
            if is_number(t):
                stack.append(TRANS_INT_Q(int(t)))
            elif 'x' in t:
                stack.append(TRANS_STR_P(t))
            else:
                raise SyntaxError
    return stack[-1]


def eval_rpn_n(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '//', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '//':
                stack.append(a // b)
            elif t == '%':
                stack.append((a % b))
        else:
            stack.append(TRANS_INT_N(int(t)))

    return stack[-1]

def eval_rpn_z(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '//', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '//':
                stack.append(a // b)
            elif t == '%':
                stack.append((a % b))
        else:
            stack.append(TRANS_INT_Z(int(t)))

    return stack[-1]

def eval_rpn_q(tokens):
    stack = []

    for t in tokens:
        if t in ['+', '-', '*', '/', '//', '%']:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '/':
                stack.append(a / b)
        else:
            stack.append(TRANS_INT_Q(int(t)))

    return stack[-1]


def eval_rpn_rf(tokens):
    """
    Упрощенный вариант: парсим как полиномы, затем преобразуем
    """
    # Сначала парсим все как полиномы

    # Но нужно обработать дроби вида (poly)/(poly)
    # Для этого временно заменим '/' на специальный разделитель

    processed_expr = ""
    for token in tokens:
        if '/' in token and '(' in token and ')' in token:
            # Это дробь, оставляем как есть
            processed_expr += token + " "
        else:
            processed_expr += token + " "

    # Создаем стек для рациональных функций
    stack = []

    for token in tokens:
        if token in ['+', '-', '*', '/']:
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b

            stack.append(result)

        else:
            # Парсим как рациональную функцию
            if '/' in token:
                # Дробь вида (poly1)/(poly2)
                parts = token.split('/')
                num_str = parts[0].strip(' ()')
                denom_str = parts[1].strip(' ()')

                # Парсим числитель и знаменатель
                num_poly = eval_rpn_p(to_rpn(num_str))
                denom_poly = eval_rpn_p(to_rpn(denom_str))

                if isinstance(num_poly, Rational):
                    num_poly = TRANS_Q_P(num_poly)
                if isinstance(denom_poly, Rational):
                    denom_poly = TRANS_Q_P(denom_poly)

                # Создаем рациональную функцию
                rf = RationalFunction(num_poly, denom_poly)
                stack.append(rf)

            else:
                # Просто полином
                poly = eval_rpn_p(to_rpn(token))

                # Преобразуем в Polynomial если нужно
                if isinstance(poly, Rational):
                    poly = TRANS_Q_P(poly)

                # Создаем рациональную функцию со знаменателем 1

                one_rat = Rational(Integer(0, 0, [1]), Natural(0, [1]))
                denom = Polynomial(0, [one_rat])
                rf = RationalFunction(poly, denom)
                stack.append(rf)

    return stack[-1] if stack else None