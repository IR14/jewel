def input_check(x, type_x, condition, input_txt, err_txt):
    """
    На входе функция принимает:
        1. x - переменная, ввод которой осуществляется
        2. type_x - тип переменной (напр. 'float' или 'int')
        3. condition - условие (в выражении используется локальная переменная)
        4. input_txt - что должно вывести при вводе
        5. err_txt - что должно вывести при ошибке
    На выходе возвращается введенная переменная по заданным условиям.
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
    Считывает с клавиатуры:
        1. внутренний диаметр кольца (размер кольца)
        2. высоту заготовки (толщину кольца)
    Возвращает длину заготовки.
    """
    D_in = None
    D_in = input_check(D_in, 'float', 'x > 0', 'Введите размер кольца:', 'Данные некорректны, повторите ввод.')
    
    h = None
    h = input_check(h, 'float', 'x > 0', 'Введите толщину вашей заготовки в мм:', 'Данные некорректны, повторите ввод.')

    l = (3.1416 * (D_in + h)) # берем средний диаметр из расчета погрешности
    print('Длина вашей заготовки равна:', '%.2f' % l, 'мм')
    return l

def wax_weight():
    """
    Считывает с клавиатуры:
        1. вес восковки (мастер модели)
        2. код металла для отливки изделия
    Возвращает массу металла, требуемую на определенную восковку.
    """
    wax = None
    wax = input_check(wax, 'float', 'x > 0', 'Введите вес мастер модели:', 'Данные некорректны, повторите ввод.')
    
    # вот так должны выглядеть словари, по индексам вровень, Серебру соответствует вес 11 и код ar и так далее...
    elements = {'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
                'weight': [11, 8.93, 21.45, 8.9, 8.5, 11.5, 14, 17],
                'code': ['ar', 'c', 'p', 'b', 'l', 'au1', 'au2', 'au3']}
    
    print('Металлы и их коды, представленные в скобках:\n')
    for i in range(len(elements['code'])):
        print(elements['metals'][i], '(%s)' % elements['code'][i])

    while True: # тут весь цикл такой же, как и с wax'ом, ток условие проверки другое
        try:
            element = input('Введите код металла металла, в котором будет отливаться изделие:')
            if elements['code'].count(element) != 0: # проверяем, что введенный код вообще есть в списке кодов
                break
            else:
                raise ValueError
        except ValueError:
            print('Код металла не распознан, повторите ввод.')
    
    # тут мозг ломается, но я объясню:
    # elements['weight'] - названия металлов, тогда, например, elements['weight'][0] - это Серебро
    # но вместо обычного 0 нам нужно запихнуть индекс кода, т.к. по индексу кода можно узнать и вес, и металл
    # elements['code'].index(element) - вернет индекс element в списке elements['code']
    # значит elements['weight'][elements['code'].index(element)] - это удельная плотность введенного металла
    print('\nМасса металла, требуемая на определенную восковку: %.2f' % (wax * elements['weight'][elements['code'].index(element)]))
    return (wax * elements['weight'][elements['code'].index(element)]) # о да, сама гениальность


def wire():
    """
    Ввод с клавиатруы:
    1. Выбор сечения
    2. Ввод массы
    3. Выбор материала
    4. Ввод двух известных параметров (длина, ширина, высота) будущей проволки.
    Возвращает максимально возможную длину проволоки(квадратного, круглого сечения) в том же материале.
    (Длина l, Ширина b; высота h, плотоность указана в г/см^3)

    """
    type_of_workpiece = None
    type_of_workpiece = input_check(type_of_workpiece, 'str', "x in ('квадратное', 'круглое')",
                                    'Введите тип сечения (круглое, квадратное):', 'Данные некорректны, повторите ввод.')

    m = None
    m = input_check(m, 'float', 'x > 0', 'Введите массу заготовки:', 'Данные некорректны, повторите ввод')

    elements = {'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
                'p': [10.36, 8.92, 21.45, 8.8, 8.6, 11.54, 13.6, 15.45],
                'code': ['ar', 'c', 'p', 'b', 'l', 'au1', 'au2', 'au3']}
    print('Металлы и их коды, представленные в скобках:\n')
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

    if type_of_workpiece == 'квадратное':

        b = None
        b = input_check(b, 'float', 'x > 0', 'Введите ширину заготовки:', 'Данные некорректны, повторите ввод')

        h = None
        h = input_check(h, 'float', 'x > 0', 'Введите высоту завготовки:', 'Данные некорректны, повторите ввод')

        print('Длина проволоки равна: %.3f' % (m / elements['p'][elements['code'].index(element)]) / (b * h))
        return (m / elements['p'][elements['code'].index(element)]) / (b * h)

    if type_of_workpiece == 'круглое':
        d = None
        d = input_check(d, 'float', 'x > 0', 'Введите диаметр заготовки:', 'Данные некорректны, повторите ввод')

        r = d / 2

        print('Длина проволоки равна: %.3f' % ((m / elements['p'][elements['code'].index(element)]) / (3.1416 * r ** 2))) 
        return ((m / elements['p'][elements['code'].index(element)]) / (3.1416 * r ** 2))
    
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
