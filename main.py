import random

import streamlit as st
import SessionState
import os


from bokeh.plotting import figure
from bokeh.models import HoverTool
from algorithms import ScheduleTask
from functions import create_file_with_condition, markdown2string, parse_condition_csv, generate_random_condition, \
    configure_height4graph_from_condition

import time


def file_selector(folder_path='./data/input_files'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Оберіть файл', filenames)
    return os.path.join(folder_path, selected_filename)


def show_answer(condition, method='Жадібний алгоритм №1', write_to_db=False):
    st.write('<h2>Відповідь</h2>',  unsafe_allow_html=True)

    start = time.time()
    task = ScheduleTask(condition)
    if method == 'Жадібний алгоритм №1':
        task.greedy_algorithm_1()
    elif method == 'Жадібний алгоритм №2':
        task.greedy_algorithm_2()
    elif method == 'Жадібний алгоритм №3':
        task.greedy_algorithm_3()
    elif method == 'Бджолиний алгоритм':
        task.bee_algorithm()


    execution_time = time.time() - start


    st.write('Метод розв\'язання - "{}"'.format(task.solution_method))
    if (method =='Бджолиний алгоритм'):
        st.write('Номер першого найкращого роз\'язку -  {}.'.format(task.best_index1))
        st.write('Значення цільової функції першого найкращого роз\'язку -  {}.'.format(task.best_target1))
        st.write('Значення вектора штрафів першого найкращого роз\'язку -  {}.'.format(task.best_U1))
        st.write('Порядок виконання робіт для першого найкращого роз\'язку -  {}.'.format(task.best_order1))
        st.write('Номер другого найкращого роз\'язку -  {}.'.format(task.best_index2))
        st.write('Значення цільової функції другого найкращого роз\'язку -  {}.'.format(task.best_target2))
        st.write('Значення вектора штрафів другого найкращого роз\'язку -  {}.'.format(task.best_U2))
        st.write('Порядок виконання робіт для другого найкращого роз\'язку -  {}.'.format(task.best_order2))
    st.write('Час виконання {} сек.'.format(execution_time))
    st.write('Значення цільової функції = {}.'.format(task.tf_res))
    st.write('Порядок виконання робіт X={}.'.format(task.order))
    st.write('Вектор штрафів U={}'.format(task.U))

    #pss = configure_height4graph_from_condition(task.schedule, task.order)
    # # st.write(pss)
    _tools_to_show = 'box_zoom,pan,save,hover,reset,tap,wheel_zoom'
    p = figure(height=200, tools=_tools_to_show)
    cur_time = 0
    for i in task.order:
        p.line([cur_time , cur_time + task.schedule[i][2]], [i, i],
               color='red' if task.U[i] == 1 else 'green',
               line_width=4, line_dash="solid")
        cur_time += task.schedule[i][2]
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Start", "@x"), ]
    hover.mode = 'mouse'

    st.bokeh_chart(p)
    st.write('На графіку червоні проміжки відповідають роботам із запізненням, зеленим - роботам без запізнення.')


def chart_page():

    st.markdown('''## Оцінка емпіричної складності алгоритмів

На наступних графіках продемонстровано залежність часу 
виконання алгоритму від кількості робіт.

### Жадібний алгоритм №1

Як можна побачити на малюнку, жадібний алгоритм #1 емпірично має складність 
$O(N) = N * log(N)$ 

\nДля 5000 робіт:''')
    st.image('data/images/Execution_greedy1_5000.png')
    st.write('Для 8000 робіт:')
    st.image('data/images/Execution_greedy1_8000.png')

    st.markdown('''
### Жадібний алгоритм #2
Як можна побачити на малюнку, жадібний алгоритм #2 емпірично має складність 
$O(N) = log(N)$ 
\nДля 5000 робіт:''')
    st.image('data/images/Execution_greedy2_5000.png')
    st.write('Для 8000 робіт:')
    st.image('data/images/Execution_greedy2_8000.png')

    st.markdown('''
### Жадібний алгоритм #3
Як можна побачити на малюнку, жадібний алгоритм #3 емпірично має складність 
$O(N) = N * log(N)$
\nДля 5000 робіт:''')
    st.image('data/images/Execution_greedy3_5000.png')
    st.write('Для 8000 робіт:')
    st.image('data/images/Execution_greedy3_8000.png')

    st.markdown('''
    
    ### Бджолиний алгоритм 
Як можна побачити на малюнку, бджолиний алгоритм емперично має складність 
$O(N) = N * log(N)$
\nДля 5000 робіт:''')
    st.image('data/images/Execution_bee_5000.png')
    st.write('Для 8000 робіт:')
    st.image('data/images/Execution_bee_8000.png')

    st.markdown('''

Для наглядності зобразимо роботу усіх трьох алгоритмів на одному графіку
\nДля 6000 робіт:''')
    st.image('data/images/Execution_6000.png')


    st.markdown('''
### Порівняння точності алгоритмів
Для подальшого аналізу візьмемо розв’язок бджолиного алгоритму, як оптимальний для даної задачі, та порівняємо з ним розв’язки інших алгоритмів 
\nДля 8000 робіт:
        ''')
    st.image('data/images/Deviation.png')




def solution_page():
    st.title('Сторінка з розв\'язанням задачі')

    session_state = SessionState.get(choose_button=False, input_type='', random='', file='', db='')
    session_state.input_type = st.selectbox('Оберіть спосіб вхідних даних', ['З файлу', 'Рандомізовано'])

    if session_state.input_type == 'Рандомізовано':
        quantity = st.number_input('Кількість робіт', step=1, value=50, min_value=1, max_value=500)
        work_end = st.number_input('Кінець роботи машини', step=1, value=1000, min_value=1, max_value=1000)

        min_fine = st.number_input('Мінімальний штраф', step=1, value=10, min_value=1, max_value=1000)
        max_fine = st.number_input('Максимальний штраф', step=1, value=100, min_value=1, max_value=1000)

        min_execution_time = st.number_input('Мінімальний термін виконання роботи', step=1,
                                             value=5, min_value=1, max_value=1000)
        max_execution_time = st.number_input('Максимальний термін виконання роботи', step=1,
                                             value=40, min_value=1, max_value=1000)

        method = st.selectbox('Оберіть метод вирішення задачі',
                              ['Жадібний алгоритм №1',
                               'Жадібний алгоритм №2',
                               'Жадібний алгоритм №3',
                               'Бджолиний алгоритм']
                              )

        if st.button('Розв\'язати'):
            condition = generate_random_condition(quantity, work_end, min_fine, max_fine,
                                                  min_execution_time, max_execution_time)
            show_answer(condition, method)
            st.table(condition2table(condition))

    if session_state.input_type == 'З файлу':
        filename = file_selector()
        # st.write('Ви обрали `%s`' % filename)
        condition = parse_condition_csv(filename)
        st.table(condition2table(condition))
        method = st.selectbox('Оберіть метод вирішення задачі',
                              ['Жадібний алгоритм №1',
                               'Жадібний алгоритм №2',
                               'Жадібний алгоритм №3',
                               'Бджолиний алгоритм']
                              )
        if st.button('Розв\'язати'):
            show_answer(condition, method)


@st.cache(allow_output_mutation=True)
def get_condition_state():
    return []


def condition2table(condition):
    a, b, c = [], [], []
    for i in condition:
        a.append(i[0])
        b.append(i[1])
        c.append(i[2])

    return {'Кінцевий термін здачі': a, 'Штраф': b, 'Тривалість виконання': c}


def create_condition_page():
    st.title('Сторінка для створення власної умови задачі')
    annotation = get_condition_state()
    if st.button('Додати роботу'):
        annotation.append(tuple())

    if st.button('Видалити останню роботу'):
        annotation.pop(len(annotation) - 1)

    for i in range(len(annotation)):
        st.subheader('Робота №{}'.format(i + 1))
        a = st.number_input('Кінцевий термін здачі {}-ої роботи'.format(i + 1), step=1, value=5, min_value=0,
                            max_value=10000)
        b = st.number_input('Штраф {}-ої роботи'.format(i + 1), step=1, value=20, min_value=0, max_value=10000)
        c = st.number_input('Тривалість виконання {}-ої роботи'.format(i + 1), step=1, value=20, min_value=0, max_value=10000)
        annotation[i] = (a, b, c)

    if st.button('Створити'):
        create_file_with_condition(annotation)


def main():
    st.sidebar.title("Оберіть сторінку:")
    pages = ['Розв\'язати задачу', 'Створити умову', 'Результати досліджень']
    counter = 0
    page = st.sidebar.selectbox("Навігація", options=pages)

    if page == 'Розв\'язати задачу':
        solution_page()

    if page == 'Створити умову':
        create_condition_page()
    if page == 'Результати досліджень':
        chart_page()


if __name__ == '__main__':
    main()

    st.markdown('<style>body{background-color: #fcd9dc;} *{font-family:"Comic Sans MS", cursive, sans-serif;}</style>', unsafe_allow_html=True)
