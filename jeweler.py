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
    diameter_inner = input_check(diameter_inner, 'float', 'x > 0', 'Введите размер кольца:', 'Данные некорректны, повторите ввод.')
    
    height = None
    height = input_check(height, 'float', 'x > 0', 'Введите толщину вашей заготовки в мм:', 'Данные некорректны, повторите ввод.')

    length = (3.1416 * (diameter_inner + height)) # берем средний диаметр из расчета погрешности
    print('Длина вашей заготовки равна: %.3f мм' % length)
    return l

def wax_weight():
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
                'weight': [11, 8.93, 21.45, 8.9, 8.5, 11.5, 14, 17],
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
    
    mass = weight * elements['weight'][elements['code'].index(element)]
    print('\nМасса металла, требуемая на определенную восковку: %.2f' % mass)
    return mass

def wire():
    """
    Input:
        1. Тип сечения
        2. Масса заготовки
        3. Металл для изготовления
        4. Ввод двух известных параметров (длина, ширина, высота) будущей проволки
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
        metric_1 = input_check(metric_1, 'float', 'x > 0', 'Введите 1-ый известный размер заготовки:', 'Данные некорректны, повторите ввод.')

        metric_2 = None
        metric_2 = input_check(metric_2, 'float', 'x > 0', 'Введите 2-ой известный размер заготовки:', 'Данные некорректны, повторите ввод.')

        print('Длина проволоки равна: %.3f' % ((mass / elements['density'][elements['code'].index(element)]) / (metric_1 * metric_2)))
        return ((mass / elements['density'][elements['code'].index(element)]) / (metric_1 * metric_2))

    else:
        
        metric_1 = None
        metric_1 = input_check(metric_1, 'float', 'x > 0', 'Введите диаметр заготовки:', 'Данные некорректны, повторите ввод.')

        print('Длина проволоки равна: %.3f' % ((mass / elements['density'][elements['code'].index(element)]) / (3.1416 * (metric_1 / 2) ** 2))) 
        return ((mass / elements['density'][elements['code'].index(element)]) / (3.1416 * (metric_1 / 2) ** 2))
    
def plate():
    """
    1. Ввод рамеров пластины(ширина (b), длина (l), высота(h))
    2. Ввод итоговой ширины и длины до которых будет прокатываться пластина.
        Вывод толщины при параметрах пункта №2
    """
    elements = {'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
                'p': [10.36, 8.92, 21.45, 8.8, 8.6, 11.54, 13.6, 15.45],
                'code': ['ar', 'c', 'p', 'b', 'l', 'au1', 'au2', 'au3']}
    print('Металлы и их коды, представленные в скобках:\n')
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

    b = None
    b = input_check(b, 'float', 'x > 0', 'Введите ширину пластины по заданным параметрам:', 'Данные некорректны, повторите ввод')

    l = None
    l = input_check(l, 'float', 'x > 0', 'Введите длину пластины по заданным параметрам:', 'Данные некорректны, повторите ввод')

    m = None
    m = input_check(m, 'float', 'x > 0', 'Введите массу пластины:', 'Данные некорректны, повторите ввод')

    print('Высота пластины: %.3f' % ((m / elements['p'][elements['code'].index(element)] / l * b)))
    return ((m / elements['p'][elements['code'].index(element)] / l * b))

def gems():
    """
    ЕСЛИ НИГДЕ НЕ ЮЗАЕМ ПАРАМЕТРЫ ФУНКЦИИ workpiece_length, то заменить их на вызов функции

        1. Вводит начальные данные, вводится длина заготовки, по заданным параметрам.
        2. Расположение камней(частично или по всей длине)
        3. Для кольца или не для кольца
        4. Показывает картинку, с макс. кол-вом камней, для текущ случая, (предлагает изменить начальные параметры, по представленным вариантам)((изменить толщину, что бы вставить недостающий камень, но если толщина конченная, сказать что это бред))
        5. Выбор увеличить расстояние между камнями или уменьшить кол-во камней
        6. Ползунок выбора расстояния между камнями(возможен выбор других опций)
        7. Кнопка завершения(адекватные решения, повторят все данные, показывает как все выглядит, итоговый результат)
    length_workpiece = int(input())
    width_workpiece = int(input())
    height_workpiece = int(input())
    d_stone = int(input()) #диаметр камушка
    """
    finger_size = None
    finger_size = input_check(finger_size, 'float', 'x > 0',
                              'Введите размер кольца:',
                              'Данные некорректны, повторите ввод.')

    height_workpiece = None
    height_workpiece = input_check(height_workpiece, 'float', 'x > 0',
                                   'Введите высоту шинки:',
                                   'Данные некорректны, повторите ввод.')

    diameter_stone = None
    diameter_stone = input_check(diameter_stone, 'float', 'x > 0',
                                 'Введите даметр камушка:',
                                 'Данные некорректны, повторите ввод.')

    print('Выберите область посадки камней.\n',
          'Выберите цифру, которая соответсвует вашему выбору:\n',
          '1. Камни расположены на четверти кольца.\n',
          '2. Камни расположены на половине кольца.\n',
          '3. Камни расположены на 3/4 кольца.\n',
          '4. Камни расположены по всей длине окружности.\n', sep='')

    code = None
    code = input_check(code, 'int', 'x in (1, 2, 3, 4)',
                       'Ввведите цифру:',
                       'Данные некорректны, повторите ввод.')

    length = code / 4 * 3.1416 * (finger_size + height_workpiece)

    num = round((length + 0.2) / (diameter_stone + 0.2))
    """
    заменить все на вызов функции, организовать базис рекурсии
    если length = None, то вызов расчета, иначе игнор
    если флаг опущен, то считываем диаметр камушка, а иначе игнор + игнор принта с кодом

    # в конце диалог с пользователем об изменении возможного количества камней
    или об изменении расстояния между камнями

    ЗДЕСЬ РИСУНОК ОКРУЖНОСТИ, ТЕКУЩЕЕ РАСПОЛОЖЕНИЕ КАМНЕЙ + ОБЛАСТЬ ПОСАДКИ
    РеКурСиЯ для показа других возможных вариантов
    """
    return num

def gems_rec(length=None):
    if length == None:
        diameter_stone = None
        diameter_stone = input_check(diameter_stone, 'float', 'x > 0',
                                     'Введите даметр камушка:',
                                     'Данные некорректны, повторите ввод.')

        print('Выберите область посадки камней.\n',
              'Выберите цифру, которая соответсвует вашему выбору:\n',
              '1. Камни расположены на четверти кольца.\n',
              '2. Камни расположены на половине кольца.\n',
              '3. Камни расположены на 3/4 кольца.\n',
              '4. Камни расположены по всей длине окружности.\n', sep='')

        code = None
        code = input_check(code, 'int', 'x in (1, 2, 3, 4)',
                           'Ввведите цифру:',
                           'Данные некорректны, повторите ввод.')

        length = code / 4 * workpiece_length()

        num = round((length + 0.2) / (diameter_stone + 0.2))

    print('lol')  # предложить увеличить расстояние или уменьшить количество камней
    """
    заменить все на вызов функции, организовать базис рекурсии
    если length = None, то вызов расчета, иначе игнор
    если флаг опущен, то считываем диаметр камушка, а иначе игнор + игнор принта с кодом

    # в конце диалог с пользователем об изменении возможного количества камней
    или об изменении расстояния между камнями

    ЗДЕСЬ РИСУНОК ОКРУЖНОСТИ, ТЕКУЩЕЕ РАСПОЛОЖЕНИЕ КАМНЕЙ + ОБЛАСТЬ ПОСАДКИ
    РеКурСиЯ для показа других возможных вариантов
    """
    return num

print('Вас приветствует самопальная программа выполненная двумя энтузиастами.\n',
      'Выберите цифру, которая соответсвует вашему выбору.\n',
       '1. Узнать длину заготовки(кольца).\n',
       '2. Пересчет массы восковки в массу металла.\n',
       '3. Пересчет массы в длину проволки разных сечений. \n',
       '4. Толщина пластины при заданных размерах.\n', sep='')
num = None
num = input_check(num, 'int', 'x in (1, 2, 3, 4)', 
                  'Ввведите цифру:',
                  'Данные некорректны, повторите ввод.')

if num == 1:
    length = workpiece_length()
elif num == 2:
    weigth = wax_weight()
elif num == 3:
    wire = wire()
elif num == 4:
    plate = plate()
