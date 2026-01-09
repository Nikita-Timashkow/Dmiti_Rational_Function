import time
import matplotlib.pyplot as plt
from P.Polynomial import Polynomial
from Q.Rational import Rational
from Z.Integer import Integer
from N.Natural import Natural


def test_single_case(degree, max_coeff=10, common_degree=2, iterations=100):
    """
    Тестирует три алгоритма на полиномах заданной степени.
    Возвращает словарь с временами выполнения.
    """
    P, Q, _ = create_polynomials_with_common_factor(
        degree, degree, common_degree, max_coeff
    )

    algorithms = [
        ('I_GCF_PP_P', lambda: P.I_GCF_PP_P(Q)),
        ('GCF_PP_P', lambda: P.GCF_PP_P(Q)),
        ('M_GCF_PP_P', lambda: P.M_GCF_PP_P(Q))
    ]

    results = {'degree': degree, 'times': {}}

    for name, func in algorithms:
        for _ in range(5):
            func()

        start = time.perf_counter()
        for _ in range(iterations):
            result = func()
        end = time.perf_counter()

        total_time = (end - start) * 1000
        avg_time = total_time / iterations

        results['times'][name] = avg_time
        results['result'] = result


    return results


def plot_comparison_graph(test_results_list):
    """
    Строит один график с тремя цветными линиями.
    """
    if not test_results_list:
        print("Нет данных для графика")
        return

    degrees = [res['degree'] for res in test_results_list]

    times_i = [res['times'].get('I_GCF_PP_P', 0)/1000 for res in test_results_list]
    times_g = [res['times'].get('GCF_PP_P', 0)/1000 for res in test_results_list]
    times_f = [res['times'].get('M_GCF_PP_P', 0)/1000 for res in test_results_list]

    plt.figure(figsize=(16, 10))

    plt.plot(degrees, times_i, color='blue', label='I_GCF_PP_P', linewidth=2)
    plt.plot(degrees, times_g, color='green', label='GCF_PP_P', linewidth=2)
    plt.plot(degrees, times_f, color='red', label='M_GCF_PP_P', linewidth=2)

    plt.xlabel('Степень полинома', fontsize=12)
    plt.ylabel('Время выполнения (c)', fontsize=12)
    plt.title('Сравнение производительности алгоритмов НОД', fontsize=14, fontweight='bold')

    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=11, loc='upper left')

    plt.tight_layout()
    plt.show()




def run_comprehensive_test():
    """Запускает комплексный тест и строит график"""

    test_degrees = [2,3,4,5,6,7,8,9,10]
    all_results = []

    for degree in test_degrees:
        iterations = max(30 - degree , 3)
        results = test_single_case(degree, max_coeff=10, iterations=iterations)
        all_results.append(results)

    plot_comparison_graph(all_results)


def create_test_polynomial(degree, max_coeff=10):
    import random
    coeffs = []
    for i in range(degree + 1):
        num = random.randint(1, max_coeff)
        den = random.randint(1, max_coeff)
        coeff = Rational(Integer(0, 0, [num]), Natural(0, [den]))
        coeffs.append(coeff)
    return Polynomial(degree, coeffs)


def create_polynomials_with_common_factor(degree1, degree2, common_degree=2, max_coeff=10):
    common = create_test_polynomial(common_degree, max_coeff)
    P_part = create_test_polynomial(degree1 - common_degree, max_coeff)
    Q_part = create_test_polynomial(degree2 - common_degree, max_coeff)
    P = P_part * common
    Q = Q_part * common
    return P, Q, common


if __name__ == "__main__":
    run_comprehensive_test()
