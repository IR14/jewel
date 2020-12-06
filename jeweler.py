import matplotlib.pyplot as plt
import numpy as np

def input_check(x, type_x, condition, input_txt, err_txt):
    """
    Input:
        1. x - переменная, ввод которой осуществляется
        2. type_x - тип переменной (напр. 'float' или 'int')
        3. condition - условие (в выражении используется локальная переменная, т.е x)
        4. input_txt - что должно вывести при вводе
        5. err_txt - что должно вывести при ошибке
    Output:
        1. Введенная переменная x по заданным условиям.
    """
    while True:
        try:
            x = eval(type_x)(input(input_txt))
            if eval(condition):
                return x
            else:
                raise ValueError
        except ValueError:
            print(err_txt)


def workpiece_length():
    """
    Input:
        1. Внутренний диаметр кольца (размер кольца)
        2. Высота заготовки (толщина кольца)
    Output:
        1. Длина заготовки
    """
    diameter_inner = None
    diameter_inner = input_check(diameter_inner, 'float', 'x > 0', 'Введите размер кольца:',
                                 'Данные некорректны, повторите ввод.')

    height = None
    height = input_check(height, 'float', 'x > 0', 'Введите толщину вашей заготовки в мм:',
                         'Данные некорректны, повторите ввод.')

    length = (3.1416 * (diameter_inner + height))  # берем средний диаметр из расчета погрешности
    print('Длина вашей заготовки равна: %.3f мм' % length)
    return length


def wax_mass():
    """
    Input:
        1. Вес восковки (мастер модели)
        2. Код металла для отливки изделия
    Output:
        1. Масса металла, требуемая на определенную восковку
    """
    weight = None
    weight = input_check(weight, 'float', 'x > 0', 'Введите вес мастер модели:', 'Данные некорректны, повторите ввод.')

    elements = {'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
                'weight_specific': [11, 8.93, 21.45, 8.9, 8.5, 11.5, 14, 17],
                'code': ['ar', 'c', 'p', 'b', 'l', 'au1', 'au2', 'au3']}

    print('\nМеталлы и их коды, представленные в скобках:\n')
    for i in range(len(elements['code'])):
        print(elements['metals'][i], '(%s)' % elements['code'][i])

    while True:
        try:
            element = input('Введите код металла металла, в котором будет отливаться изделие:')
            if elements['code'].count(element) != 0:
                break
            else:
                raise ValueError
        except ValueError:
            print('Код металла не распознан, повторите ввод.')

    mass = weight * elements['weight_specific'][elements['code'].index(element)]
    print('\nМасса металла, требуемая на определенную восковку: %.2f' % mass)
    return mass


def wire():
    """
    Input:
        1. Тип сечения
        2. Масса заготовки
        3. Металл для изготовления
        4. Два известных параметра будущей проволки из списка: (длина, ширина, высота)
    Output:
        1.1. Максимальная возможная длина проволоки для квадратного сечения
        1.2. Максимальная возможная длина проволоки для круглого сечения
    """
    type_of_workpiece = None
    type_of_workpiece = input_check(type_of_workpiece, 'int', 'x in (1, 2)',
                                    'Выберите цифру, которая соответсвует вашему выбору:\n1. Квадратное сечение.\n2. Круглое сечение.\n',
                                    'Данные некорректны, повторите ввод.')

    mass = None
    mass = input_check(mass, 'float', 'x > 0', 'Введите массу заготовки:', 'Данные некорректны, повторите ввод')

    elements = {'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
                'density': [10.36, 8.92, 21.45, 8.8, 8.6, 11.54, 13.6, 15.45],
                'code': ['ar', 'c', 'p', 'b', 'l', 'au1', 'au2', 'au3']}

    print('\nМеталлы и их коды, представленные в скобках:\n')
    for i in range(len(elements['code'])):
        print(elements['metals'][i], '(%s)' % elements['code'][i])

    while True:
        try:
            element = input('Введите код металла металла проволоки:')
            if elements['code'].count(element) != 0:
                break
            else:
                raise ValueError
        except ValueError:
            print('Код металла не распознан, повторите ввод.')

    if type_of_workpiece == 1:

        metric_1 = None
        metric_1 = input_check(metric_1, 'float', 'x > 0', 'Введите 1-ый известный размер заготовки:',
                               'Данные некорректны, повторите ввод.')

        metric_2 = None
        metric_2 = input_check(metric_2, 'float', 'x > 0', 'Введите 2-ой известный размер заготовки:',
                               'Данные некорректны, повторите ввод.')

        length = (mass / elements['density'][elements['code'].index(element)]) / (metric_1 * metric_2)

    else:

        metric_1 = None
        metric_1 = input_check(metric_1, 'float', 'x > 0', 'Введите диаметр заготовки:',
                               'Данные некорректны, повторите ввод.')

        length = (mass / elements['density'][elements['code'].index(element)]) / (3.1416 * (metric_1 / 2) ** 2)

    print('Длина проволоки равна: %.3f' % length)
    return length


def plate():
    """
    Input:
        1. Два известных параметра будущей платины из списка: (длина, ширина, высота)
        2. Масса пластины
    Output:
        1. 3-ий (неизвестный) размер пластины
    """
    elements = {'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
                'density': [10.36, 8.92, 21.45, 8.8, 8.6, 11.54, 13.6, 15.45],
                'code': ['ar', 'c', 'p', 'b', 'l', 'au1', 'au2', 'au3']}

    print('\nМеталлы и их коды, представленные в скобках:\n')
    for i in range(len(elements['code'])):
        print(elements['metals'][i], '(%s)' % elements['code'][i])

    while True:
        try:
            element = input('Введите код металла металла пластины:')
            if elements['code'].count(element) != 0:
                break
            else:
                raise ValueError
        except ValueError:
            print('Код металла не распознан, повторите ввод.')

    metric_1 = None
    metric_1 = input_check(metric_1, 'float', 'x > 0', 'Введите 1-ый известный размер пластины:',
                           'Данные некорректны, повторите ввод.')

    metric_2 = None
    metric_2 = input_check(metric_2, 'float', 'x > 0', 'Введите 2-ой известный размер пластины:',
                           'Данные некорректны, повторите ввод.')

    mass = None
    mass = input_check(mass, 'float', 'x > 0', 'Введите массу пластины:', 'Данные некорректны, повторите ввод.')

    metric_3 = mass / elements['density'][elements['code'].index(element)] / metric_1 / metric_2
    print('Неизвестный 3-ий размер пластины: %.3f' % metric_3)
    print('3-ий размер - это высота, если были введены ширина и длина и т.д.')
    return metric_3


def point(radius_outer_ring, radius_stone):
    """
    Input:
        1. Радиус внешнего кольца
        2. Радиус камня для инкрустации
    Output:
        1. Высота, относительно центра кольца, на которой расположены пересечения камня с внешним кольцом
    """
    return .5 * (2 * radius_outer_ring ** 2 - radius_stone ** 2) / radius_outer_ring
    # h = (radius_outer_ring ** 2 - a ** 2) ** .5


def ring(finger_size, height_workpiece, diameter_stone, code, num, distance):
    """
    Input:
        1. Размер кольца (пальца) (диаметр)
        2. Высота заготовки
        3. Диаметр инкрустированного камня
        4. Область посадки камней на кольце
        5. Количество камней
        6. Расстояние между камнями
    Output:
        1. Рисунок кольца по заданным параметрам
    """
    circle_inner = plt.Circle((0, 0), .5 * finger_size, fill=False, color='pink', linewidth=2)
    circle_outer = plt.Circle((0, 0), .5 * finger_size + height_workpiece, fill=False, color='pink', linewidth=2)

    fig, ax = plt.subplots()

    plt.xlim(-.5 * finger_size - 2 * height_workpiece, .5 * finger_size + 2 * height_workpiece)
    plt.ylim(-.5 * finger_size - 2 * height_workpiece, .5 * finger_size + 2 * height_workpiece)

    ax.set_aspect(1)

    plt.grid(linestyle='--')

    coordinates = {'x': [], 'y': []}

    alpha = .5 * np.pi * code - np.arccos(
        point(.5 * finger_size + height_workpiece, .5 * diameter_stone) / (.5 * finger_size + height_workpiece))

    beta = np.arccos(point(.5 * finger_size + height_workpiece, .5 * distance) / (
            .5 * finger_size + height_workpiece)) - 2 * alpha + np.pi * code

    for i in range(num):
        coordinates['x'].append((.5 * finger_size + height_workpiece) * np.cos(alpha))
        coordinates['y'].append((.5 * finger_size + height_workpiece) * np.sin(alpha))
        alpha -= beta

    for i in range(len(coordinates['x'])):
        ax.add_artist(
            plt.Circle((coordinates['x'][i], coordinates['y'][i]),
                       .5 * diameter_stone,
                       fill=True,
                       color='salmon',
                       linewidth=0))

    ax.add_artist(circle_inner)
    ax.add_artist(circle_outer)

    plt.show()


def gems(length, flag_height_workpiece, flag_diameter_stone, flag_code, flag_num, flag_distance, finger_size,
         height_workpiece, diameter_stone, distance, code):
    """
    Рекурсивная функция обработки параметров для визуализации кольца.
    Input:
        1. Длина внешнего кольца
        2. Флаг изменения высоты заготовки
        3. Флаг изменения диаметра инкрустированного камня
        4. Флаг изменения области посадки камней
        5. Флаг изменения количества камней (и есть их количество)
        6. Флаг изменения расстояния между камнями
        7. Размер кольца (пальца) (диаметр)
        8. Высота заготовки
        9. Диаметр инкрустированного камня
        10. Расстояние между камнями
        11. Область посадки камней на кольце
    Output:
        1. Вызов функции визуализации ring по заданным параметрам
        2. Контроль изменения параметров для повторной визуализации
    """
    if not length:
        finger_size = None
        finger_size = input_check(finger_size, 'float', 'x > 0',
                                  'Введите размер кольца:',
                                  'Данные некорректны, повторите ввод.')

    if flag_height_workpiece or not length:
        if not length:
            height_workpiece = None
        height_workpiece = input_check(height_workpiece, 'float', 'x > 0',
                                       'Введите высоту шинки:',
                                       'Данные некорректны, повторите ввод.')

    if flag_diameter_stone or not length:
        while True:
            try:
                diameter_stone = float((input('Введите диаметр камушка, который находится в промежутке от 0.5 до %f:'
                                              % (2 * (height_workpiece - .8)))))
                if (diameter_stone >= .5) and (diameter_stone <= 2 * (height_workpiece - .8)):
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Данные некорректны, повторите ввод.')

    if flag_distance or not length:
        if not length:
            distance = None
        distance = input_check(distance, 'float', 'x >= .2',
                               'Введите расстояние между камнями, минимально значение это 0.2 (Количество камней может измениться!):',
                               'Данные некорректны, повторите ввод.')

    if flag_code or not length:
        print('Выберите область посадки камней.\n',
              'Выберите цифру, которая соответсвует вашему выбору:\n',
              '1. Камни расположены на четверти кольца.\n',
              '2. Камни расположены на половине кольца.\n',
              '3. Камни расположены на 3/4 кольца.\n',
              '4. Камни расположены по всей длине окружности.\n', sep='')
        if not length:
            code = None
        code = input_check(code, 'int', 'x in (1, 2, 3, 4)',
                           'Ввведите цифру:',
                           'Данные некорректны, повторите ввод.')

    if flag_code or flag_height_workpiece or not length:
        length = code / 2 * np.pi * (.5 * finger_size + height_workpiece)

    max_num = round(length / (diameter_stone + distance))
    # (всегда будет измен. если изм. друг. парм.)максимальное кол-во камней для функции ring()

    if not flag_num:
        ring(finger_size, height_workpiece, diameter_stone, code, max_num, distance)
    else:
        ring(finger_size, height_workpiece, diameter_stone, code, flag_num, distance)

    flag_height_workpiece, flag_diameter_stone, flag_code, flag_num, flag_distance = False, False, False, False, False

    print('Выберите дальнейшие действия.\n',
          'Вы можете выбрать комбинацию действий, например, чтобы одновременно изменить высоту заготовки и область посадки камней,\
          необходимо ввести «13».\n',
          'Выберите цифру, которая соответсвует вашему выбору:\n',
          '1. Изменить высоту заготовки.\n',
          '2. Изменить диаметр камня.\n',
          '3. Изменить область посадки камней.\n',
          '4. Изменить количество камней.\n',
          '5. Изменить расстояние между камнями.\n',
          '6. Выход.\n', sep='')

    choose = None
    choose = input_check(choose, 'int',
                         'x in (1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 23, 24, 25, 34, 35, 45, 123, 124, 125, 134, 135, 145, 234, 235, 245, 345, 1234, 1235, 1245, 1345, 2345, 12345)',
                         'Ввведите цифру:',
                         'Данные некорректны, повторите ввод.')

    if str(choose).find('6') == -1:

        if str(choose).find('1') != -1:
            flag_height_workpiece = True

        if str(choose).find('2') != -1:
            flag_diameter_stone = True

        if str(choose).find('3') != -1:
            flag_code = True

        if str(choose).find('4') != -1:
            if not flag_num:
                flag_num = None
                while True:
                    try:
                        flag_num = int(
                            (input('Введите новое количество камней, которое находится в промежутке от 1 до %d:'
                                   % (max_num - 1))))
                        if (flag_num > 0) and (flag_num < max_num):
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print('Данные некорректны, повторите ввод.')

        if str(choose).find('5') != -1:
            flag_distance = True

        gems(length, flag_height_workpiece, flag_diameter_stone, flag_code, flag_num, flag_distance, finger_size,
             height_workpiece, diameter_stone, distance, code)


print('Вас программа для математических расчетов в повседневных задачач ювелирного мастера.\n')

num = None

while True:
    print('Выберите цифру, которая соответсвует вашему выбору.\n',
          '1. Узнать длину заготовки(кольца).\n',
          '2. Пересчет массы восковки в массу металла.\n',
          '3. Пересчет массы в длину проволки разных сечений.\n',
          '4. Толщина пластины при заданных размерах.\n',
          '5. Визуализировать кольцо.\n',
          '6. Закончить работу с программой.\n', sep='')

    num = input_check(num, 'int', 'x in (1, 2, 3, 4, 5, 6)',
                      'Ввведите цифру:',
                      'Данные некорректны, повторите ввод.')
    if num == 6:
        print('Спасибо, что пользуетесь программой. Пока-пока!')
        break
    elif num == 1:
        length = workpiece_length()
    elif num == 2:
        weight = wax_mass()
    elif num == 3:
        wire = wire()
    elif num == 4:
        plate = plate()
    elif num == 5:
        gems(length=None, flag_height_workpiece=False, flag_diameter_stone=False, flag_code=False, flag_num=False,
             flag_distance=False, finger_size=None, height_workpiece = None, diameter_stone = None, distance = None, code = None)
