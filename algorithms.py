import random

SCHEDULE = [(25, 100, 5), (24, 50, 7), (20, 30, 4), (50, 80, 10), (30, 110, 14)]


class ScheduleTask:
    def __init__(self, schedules_list):
        self.schedule = schedules_list  # кінцевий срок сдачі, штраф, час виконання
        self.U = [0 for _ in schedules_list]
        self.tf_res = 0
        self.solution_method = None
        self.n = len(schedules_list)
        self.order = [-1 for _ in range(self.n)]
        self.best_index1 = 0
        self.best_target1 = 0
        self.best_index2 = 0
        self.best_target2 = 0
        self.best_U1 = [0 for _ in schedules_list]
        self.best_U2 = [0 for _ in schedules_list]
        self.best_order1 = [-1 for _ in range(self.n)]
        self.best_order2 = [-1 for _ in range(self.n)]
        self.best_target2_after_replacement = 0
        self.best_order2_after_replacement = [-1 for _ in range(self.n)]
        self.best_vector2_after_replacement = [0 for _ in schedules_list]
        self.best_target1_after_replacement = 0
        self.best_order1_after_replacement = [-1 for _ in range(self.n)]
        self.best_vector1_after_replacement = [0 for _ in schedules_list]

    def greedy_algorithm_1(self):
        self.__greedy_algorithm(lambda x: x[1] / x[2])
        self.solution_method = 'жадібний алгоритм #1'

    def greedy_algorithm_2(self):
        self.__greedy_algorithm(lambda x: x[1] / x[0])
        self.solution_method = 'жадібний алгоритм #2'

    def greedy_algorithm_3(self):
        self.__greedy_algorithm(lambda x: x[1] / (x[0] * x[2]))
        self.solution_method = 'жадібний алгоритм #3'



    def __greedy_algorithm(self, function):
        self.U = [0 for _ in self.schedule]
        self.order = [-1 for _ in range(self.n)]

        p = [() for _ in range(self.n)]
        for i in range(self.n):
            p[i] = (i, function(self.schedule[i]))

        p.sort(key=lambda x: x[1], reverse=True)
        self.order = [i[0] for i in p]

        self.count_fines_vector()
        self.tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])

    def count_fines_vector(self):
        # TODO ВОПРОС ПРО ВРЕМЯ
        time = 0
        self.U = [0 for _ in self.schedule]
        for current in self.order:
            time += self.schedule[current][2]
            if time > self.schedule[current][0]:
                self.U[current] = 1

    def random_algorithm(self):

        self.order = random.sample(range(self.n), self.n)
        self.count_fines_vector()
        self.tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])


    def bee_algorithm(self, quantity_of_random=3):

        solutions = [{} for _ in range(quantity_of_random + 3)]
        self.greedy_algorithm_1()
        solutions[0].update({
            'method': 'жадібний алгоритм #1',
            'target function': self.tf_res,
            'fine vector': self.U,
            'order': self.order
        })


        self.greedy_algorithm_2()
        solutions[1].update({
            'method': 'жадібний алгоритм #2',
            'target function': self.tf_res,
            'fine vector': self.U,
            'order': self.order
        })

        self.greedy_algorithm_3()
        solutions[2].update({
            'method': 'жадібний алгоритм #3',
            'target function': self.tf_res,
            'fine vector': self.U,
            'order': self.order
        })


        self.random_algorithm()
        solutions[3].update({
            'method': 'random1',
            'target function': self.tf_res,
            'fine vector': self.U,
            'order': self.order
        })


        self.random_algorithm()
        solutions[4].update({
            'method': 'random2',
            'target function': self.tf_res,
            'fine vector': self.U,
            'order': self.order
        })

        self.random_algorithm()
        solutions[5].update({
            'method': 'random3',
            'target function': self.tf_res,
            'fine vector': self.U,
            'order': self.order
        })

        solutions_tf_res = [{} for _ in range(len(solutions))]
        for i in range(len(solutions)):
            solutions_tf_res[i].update({
                'method target function': solutions[i]['target function'],
                 'method index': i
            })
        solutions_tf_res = sorted(solutions_tf_res, key=lambda e: e['method target function'])
        print(solutions_tf_res)

        self.best_index1 = solutions_tf_res[0]['method index']
        self.best_index2 = solutions_tf_res[1]['method index']

        fbs = solutions[self.best_index1]  # выбираю первое лучшее решение
        self.best_order1 = fbs['order']
        self.best_U1 = fbs['fine vector']
        self.best_target1 = fbs['target function']
        self.order = fbs['order']  # присвиваю главной очереди очередь первого лучшего решения
        self.U = fbs['fine vector']  # присвиваю главному вектору штрафов вектор штрафов первого лучшего решения
        self.tf_res = fbs['target function']  # присвиваю главной целевой функции функцию первого лучшего решения

        for i in range(len(self.U)):  # прохожу циклом по длине вектора штрафов
            if i < len(self.U) - 1:  # тут делаю так,что не было выхода за пределы массива
                if self.U[i] == 1 or self.U[i + 1] == 1:  # если i-тый элемент вектора штрафа или след элемент == 1, то
                    sum_of_time = 0  # объявляю суму времени
                    sum_of_deadlines = 0  # объявляю суму дедлайнов
                    for j in range(i + 2):  # прохожусь по всем элементам, которые идут до j включительно, чтоб узнать Cj и Dj (почему-то надо добавит 2, чтоб норм считало)
                        sum_of_time += self.schedule[self.order[j]][2]  # добавляю время
                        sum_of_deadlines += self.schedule[self.order[j]][0]  # добавляю дедлайны
                    time_of_pi = self.schedule[self.order[i]][2]  # присваиваю время на выполнение предыдущей работы

                    if sum_of_time - sum_of_deadlines <= time_of_pi:  # пишу эту формулу, Cj - Dj <= Pi, если выполняется то
                        tmp_tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])
                        tmp = self.order[i]
                        self.order[i] = self.order[i + 1]
                        self.order[i + 1] = tmp
                        self.tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])
                        if tmp_tf_res <= self.tf_res:
                            tmp = self.order[i]
                            self.order[i] = self.order[i + 1]
                            self.order[i + 1] = tmp
                            self.tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])

        self.count_fines_vector()  # считаю новый вектор
        self.best_vector1_after_replacement = self.U  # присваиваю новый вектор временной переменной
        self.best_target1_after_replacement = self.tf_res  # присваиваю новую целевую функцию  временной переменной
        self.best_order1_after_replacement = self.order  # присваиваю новую очередь временной переменной

        # ниже все то же самое для второго лучшего решения
        sbs = solutions[self.best_index2]
        self.best_target2 = sbs['target function']
        self.best_order2 = sbs['order']
        self.best_U2 = sbs['fine vector']
        self.order = sbs['order']
        self.U = sbs['fine vector']
        self.tf_res = sbs['target function']

        for i in range(len(self.U)):
            if i < len(self.U) - 1:
                if self.U[i] == 1 or self.U[i + 1] == 1:
                    sum_of_time = 0
                    sum_of_deadlines = 0
                    for j in range(i + 2):
                        sum_of_time += self.schedule[self.order[j]][2]
                        sum_of_deadlines += self.schedule[self.order[j]][0]
                    time_of_pi = self.schedule[self.order[i]][2]

                    if sum_of_time - sum_of_deadlines <= time_of_pi:
                        tmp_tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])
                        tmp = self.order[i]
                        self.order[i] = self.order[i + 1]
                        self.order[i + 1] = tmp
                        self.tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])
                        if tmp_tf_res <= self.tf_res:
                            tmp = self.order[i]
                            self.order[i] = self.order[i + 1]
                            self.order[i + 1] = tmp
                            self.tf_res = sum([i * j[1] for i, j in zip(self.U, self.schedule)])


        self.count_fines_vector()
        self.best_target2_after_replacement = self.tf_res
        self.best_order2_after_replacement = self.order
        self.best_vector2_after_replacement = self.U

        # проверяю, какое решение лучше и присваиваю главным переменным данные из временных
        if self.best_target2_after_replacement < self.best_target1_after_replacement:
            self.tf_res = self.best_target2_after_replacement
            self.order = self.best_order2_after_replacement
            self.U = self.best_vector2_after_replacement
        else:
            self.tf_res = self.best_target1_after_replacement
            self.order = self.best_order1_after_replacement
            self.U = self.best_vector1_after_replacement

        self.solution_method = 'Бджолиний алгоритм'
        print(self.order, self.U, self.tf_res)
if __name__ == '__main__':
    task = ScheduleTask(SCHEDULE)
    task.greedy_algorithm_1()
    print(task.order, task.U, task.solution_method, task.tf_res)

    task.greedy_algorithm_2()
    print(task.order, task.U, task.solution_method, task.tf_res)

    task.greedy_algorithm_3()
    print(task.order, task.U, task.solution_method, task.tf_res)

    task.bee_algorithm()
    print(task.U, task.solution_method, task.tf_res, task.best_target1, task.best_target2, task.best_index1,
          task.best_index2, task.best_U1, task.best_U2, task.best_order1, task.best_order2)
