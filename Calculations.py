from algorithms import ScheduleTask
import random
import timeit
import time
import math
import matplotlib.pyplot as plt
from functions import generate_random_condition

N = 8000


def generate_shedules(n):
    shedules = []

    for _ in range(n):
        b = random.randint(1, 200)
        e = random.randint(b + 1, int(50 + b))
        shedules.append((b, e))

    return shedules


def execution_time_greedy_1(shedules_task):
    start = timeit.default_timer()
    shedules_task.greedy_algorithm_1()
    end = timeit.default_timer()
    return (end - start) * 1000


def execution_time_greedy_2(shedules_task):
    start = timeit.default_timer()
    shedules_task.greedy_algorithm_2()
    end = timeit.default_timer()
    return (end - start) * 1000

def execution_time_greedy_3(shedules_task):
    start = timeit.default_timer()
    shedules_task.greedy_algorithm_3()
    end = timeit.default_timer()
    return (end - start) * 1000

def execution_time_bee(shedules_task):
    start = timeit.default_timer()
    shedules_task.greedy_algorithm_3()
    end = timeit.default_timer()
    return (end - start) * 1000

def complexity_plots():
    amounts = range(1, N + 1)

    times_greedy_1 = []
    times_greedy_2 = []
    times_greedy_3 = []
    times_bee = []

    tf_greedy_1 = []
    tf_greedy_2 = []
    tf_greedy_3 = []
    tf_bee = []

    for i in range(1, N + 1):
        # b = random.randint(1, 200)
        # e = random.randint(b, int(40 + b * 0.8))
        # exps_list.append((b, e))
        shedules_list = generate_random_condition(i, 100, 1, 100, 1, 200)
        shedules_task = ScheduleTask(shedules_list)

        times_greedy_1.append(execution_time_greedy_1(shedules_task))
        tf_greedy_1.append(shedules_task.tf_res)

        times_greedy_2.append(execution_time_greedy_2(shedules_task))
        tf_greedy_2.append(shedules_task.tf_res)

        times_greedy_3.append(execution_time_greedy_3(shedules_task))
        tf_greedy_3.append(shedules_task.tf_res)

        times_bee.append(execution_time_bee(shedules_task))
        tf_bee.append(shedules_task.tf_res)

    comp_log = [n * math.log(n, 2) / 5000 for n in amounts]
    comp_sq = [n * n / 400000 for n in amounts]
    plt.plot(amounts, times_greedy_1, amounts, comp_log, comp_sq, 'red')
    plt.legend(['f(N)', 'N*log(N)', 'N^2'])
    plt.ylabel('Execution time of Greedy Algorithm #1 (in milliseconds)')
    plt.xlabel('Amount of works')
    plt.show()

    comp_log = [n * math.log(n, 2) / 500 for n in amounts]
    comp_sq = [n * n / 30000 for n in amounts]
    plt.plot(amounts, times_greedy_2, amounts, comp_log, comp_sq, 'red')
    plt.legend(['f(N)', 'N*log(N)', 'N^2'])
    plt.ylabel('Execution time of Greedy Algorithm #2 (in milliseconds)')
    plt.xlabel('Amount of works')
    plt.show()

    comp_log = [n * math.log(n, 2) / 7000 for n in amounts]
    comp_sq = [n * n / 500000 for n in amounts]
    plt.plot(amounts, times_greedy_3, amounts, comp_log, comp_sq, 'red')
    plt.legend(['f(N)', 'N*log(N)', 'N^2'])
    plt.ylabel('Execution time of Greedy Algorithm #3 (in milliseconds)')
    plt.xlabel('Amount of works')
    plt.show()

    comp_log = [n * math.log(n, 2) / 7000 for n in amounts]
    comp_sq = [n * n / 500000 for n in amounts]
    plt.plot(amounts, times_bee, amounts, comp_log, comp_sq, 'red')
    plt.legend(['f(N)', 'N*log(N)', 'N^2'])
    plt.ylabel('Execution time of Bee Algorithm (in milliseconds)')
    plt.xlabel('Amount of works')
    plt.show()

    plt.plot(amounts, times_bee, 'mediumpurple', amounts, times_greedy_1, 'red', amounts, times_greedy_3, 'limegreen',
             amounts, times_greedy_2, 'blue')
    plt.legend(['Bee algorithm', 'Greedy #1 algorithm', 'Greedy #3 algorithm', 'Greedy #2 algorithm'])
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Amount of works')
    plt.show()

    eval_greedy1_bee = [abs(((j - i) / j) * 100) for i, j in zip(tf_greedy_1, tf_bee)]
    eval_greedy2_bee = [abs(((j - i) / j) * 100) for i, j in zip(tf_greedy_2, tf_bee)]
    eval_greedy3_bee = [abs(((j - i) / j) * 100) for i, j in zip(tf_greedy_3, tf_bee)]

    plt.plot(amounts, eval_greedy1_bee,'blue', amounts, eval_greedy2_bee, 'limegreen',  amounts, eval_greedy3_bee, 'mediumpurple')
    plt.legend(['Greedy #1 algorithm', 'Greedy #2 algorithm', 'Greedy #3 algorithm'])
    plt.ylabel('Deviation from the optimal value (in %)')
    plt.xlabel('Amount of works')
    plt.show()


def limits_plots():
    right_limits = [i * 10000 for i in range(1, 101, 10)]
    max_len = [i * 1000 for i in range(1, 101, 10)]

    times_greedy_1 = []
    times_greedy_2= []
    times_greedy_3 = []
    times_bee = []

    tf_greedy_1 = []
    tf__greedy_2= []
    tf_greedy_3 = []
    tf_bee = []

    for i, j in zip(right_limits, max_len):
        schedules_list = generate_random_condition(N, 100, 1, i, 1, j)
        schedules_task = ScheduleTask(schedules_list)

        times_greedy_1.append(execution_time_greedy_1(schedules_task))
        tf_greedy_1.append(schedules_task.tf_res)

        times_greedy_2.append(execution_time_greedy_2(schedules_task))
        tf__greedy_2.append(schedules_task.tf_res)

        times_greedy_3.append(execution_time_greedy_3(schedules_task))
        tf_greedy_3.append(schedules_task.tf_res)

        times_bee.append(execution_time_bee(schedules_task))
        tf_bee.append(schedules_task.tf_res)

    plt.plot(right_limits, times_greedy_1, 'mediumpurple', right_limits, times_greedy_2,'orange' ,right_limits, times_greedy_3,
             'limegreen',right_limits, times_bee,
             'red')
    plt.legend(['Greedy #1 algorithm', 'Greedy #1 algorithm', 'Greedy #3 algorithm', 'Bee algorithm'])
    plt.ylabel('Execution time (in milliseconds)')
    plt.xlabel('Right limit of the end point')
    plt.show()


if __name__ == '__main__':
    #limits_plots()
    complexity_plots()