import matplotlib.pyplot as plt
import numpy as np


def input_check(value, value_type, condition, input_message, err_message):
    """
    Input:
        1. Переменная, ввод которой осуществляется
        2. Тип переменной (напр. 'float' или 'int')
        3. Условие (в выражении используется локальная переменная, т.е x)
        4. Сообщение при вводе
        5. Сообщение об ошибке
    Output:
        1. Введенная переменная по заданным условиям
    """
    while True:
        try:
            value = eval(value_type)(input(input_message))
            if eval(condition):
                return value
            else:
                raise ValueError
        except ValueError:
            print(err_message)


def root_level(radius_outer_ring, radius_stone):
    """
    Input:
        1. Радиус внешнего кольца
        2. Радиус камня для инкрустации
    Output:
        1. Высота, относительно центра кольца, на которой расположены пересечения камня с внешним кольцом
    """
    return .5 * (2 * radius_outer_ring ** 2 - radius_stone ** 2) / radius_outer_ring


class Controller:
    metal_data = {
        'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
        'weight_specific': [11, 8.93, 21.45, 8.9, 8.5, 11.5, 14, 17],
        'density': [10.36, 8.92, 21.45, 8.8, 8.6, 11.54, 13.6, 15.45],
        'code': ['ar', 'c', 'p', 'b', 'l', 'au1', 'au2', 'au3']}

    _mass = None

    def __init__(self):
        self._mass = input_check(self._mass, 'float', 'value > 0', 'Введите массу заготовки:',
                                 'Данные некорректны, повторите ввод')

        self.data_representation()

        while True:
            try:
                self._element = input('Введите код металла, в котором будет отливаться изделие:')
                if self.metal_data['code'].count(self._element) != 0:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Код металла не распознан, повторите ввод.')

    def data_representation(self):
        print('\nМеталлы и их коды, представленные в скобках:\n')
        for i in range(len(self.metal_data['code'])):
            print(self.metal_data['metals'][i], '(%s)' % self.metal_data['code'][i])


class Plate(Controller):
    _mass, _metric_1, _metric_2 = None, None, None

    def __init__(self):
        super().__init__()

        self._metric_1 = input_check(self._metric_1, 'float', 'value > 0',
                                     'Введите 1-ый известный размер изделия:',
                                     'Данные некорректны, повторите ввод.')

        self._metric_2 = input_check(self._metric_2, 'float', 'value > 0',
                                     'Введите 2-ой известный размер изделия:',
                                     'Данные некорректны, повторите ввод.')

    def metric_unknown(self):
        """
        Input:
            1. Два известных параметра будущей пластины из списка: (длина, ширина, высота)
            2. Масса пластины
        Output:
            1. 3-ий (неизвестный) размер пластины
        """
        return self._mass / self.metal_data['density'][
            self.metal_data['code'].index(self._element)] / self._metric_1 / self._metric_2


class Wire(Plate):
    __type, _mass, _metric_1, _metric_2 = None, None, None, None

    def __init__(self):
        self.__type = input_check(self.__type, 'int', 'value in (1, 2)',
                                  'Выберите цифру, которая соответсвует вашему выбору:\n1. Квадратное сечение.\n2. Круглое сечение.\n',
                                  'Данные некорректны, повторите ввод.')

        if self.__type == 1:
            super().__init__()

        else:
            Controller.__init__(self)
            self._metric_1 = input_check(self._metric_1, 'float', 'value > 0',
                                         'Введите диаметр заготовки:',
                                         'Данные некорректны, повторите ввод.')

    def length_limit(self):
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
        if self.__type == 1:
            return (self._mass / self.metal_data['density'][self.metal_data['code'].index(self._element)]) / (
                    self._metric_1 * self._metric_2)
        else:
            return (self._mass / self.metal_data['density'][self.metal_data['code'].index(self._element)]) / (
                    np.pi * (self._metric_1 / 2) ** 2)

    def metric_unknown(self):
        return super().metric_unknown()


class Wax(Controller):
    """
    Input:
        1. Вес восковки (мастер модели)
        2. Код металла для отливки изделия
    Output:
        1. Масса металла, требуемая на определенную восковку
    """
    __weight = None

    def __init__(self):
        self.__weight = input_check(self.__weight, 'float', 'x > 0', 'Введите вес мастер модели:',
                                    'Данные некорректны, повторите ввод.')

        self.data_representation()

        while True:
            try:
                self.__element = input('Введите код металла металла, в котором будет отливаться изделие:')
                if self.metal_data['code'].count(self.__element) != 0:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Код металла не распознан, повторите ввод.')

    def wax_mass(self):
        mass = self.__weight * self.metal_data['weight_specific'][self.metal_data['code'].index(self.__element)]
        print('\nМасса металла, требуемая на определенную восковку: %.2f' % mass)
        return mass


class Ring:
    __finger_size, __height_workpiece, __diameter_stone, __distance, __code = None, None, None, None, None

    def __init__(self):
        self.__finger_size = input_check(self.__finger_size, 'float', 'value > 0',
                                         'Введите размер кольца:',
                                         'Данные некорректны, повторите ввод.')

        self.__height_workpiece = input_check(self.__height_workpiece, 'float', 'value > 0',
                                              'Введите высоту шинки:',
                                              'Данные некорректны, повторите ввод.')

        while True:
            try:
                self.__diameter_stone = float(
                    (input('Введите диаметр камушка, который находится в промежутке от 0.5 до %f:'
                           % (2 * (self.__height_workpiece - .8)))))
                if (self.__diameter_stone >= .5) and (self.__diameter_stone <= 2 * (self.__height_workpiece - .8)):
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Данные некорректны, повторите ввод.')

        self.__distance = input_check(self.__distance, 'float', 'value >= .2',
                                      'Введите расстояние между камнями, минимально значение это 0.2 (Количество камней может измениться!):',
                                      'Данные некорректны, повторите ввод.')

        print('Выберите область посадки камней:\n',
              '1. Камни расположены на четверти кольца.\n',
              '2. Камни расположены на половине кольца.\n',
              '3. Камни расположены на 3/4 кольца.\n',
              '4. Камни расположены по всей длине окружности.\n', sep='')

        self.__code = input_check(self.__code, 'int', 'value in (1, 2, 3, 4)',
                                  'Введите цифру, которая соответсвует вашему выбору:',
                                  'Данные некорректны, повторите ввод.')

        self.__current_num = self.num_limit()

    def workpiece_length(self):
        """
        Input:
            1. Внутренний диаметр кольца (размер пальца)
            2. Высота заготовки (толщина кольца)
        Output:
            1. Длина заготовки с учетом погрешности
        """
        length = .25 * self.__code * np.pi * (
                self.__finger_size + self.__height_workpiece)  # берем средний радиус из расчета погрешности
        print('Длина вашей заготовки равна: %.3f мм' % length)
        return length

    def num_limit(self):
        """
        Input:
            1. Длина заготовки (кольца)
            2. Диаметр камня
            3. Область между инкрустированными камнями
        Output:
            1. Максимальное количество камней, которые поместятся на выбранной области посадки
        """
        return round(self.workpiece_length() / (self.__diameter_stone + self.__distance))

    def illustrate(self):
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
        circle_inner = plt.Circle((0, 0), .5 * self.__finger_size, fill=False, color='pink', linewidth=2)
        circle_outer = plt.Circle((0, 0), .5 * self.__finger_size + self.__height_workpiece, fill=False, color='pink',
                                  linewidth=2)

        fig, ax = plt.subplots()

        plt.xlim(-.5 * self.__finger_size - 2 * self.__height_workpiece,
                 .5 * self.__finger_size + 2 * self.__height_workpiece)
        plt.ylim(-.5 * self.__finger_size - 2 * self.__height_workpiece,
                 .5 * self.__finger_size + 2 * self.__height_workpiece)

        ax.set_aspect(1)

        plt.grid(linestyle='--')

        coordinates = {'x': [], 'y': []}

        alpha = .5 * np.pi * self.__code - np.arccos(
            root_level(.5 * self.__finger_size + self.__height_workpiece, .5 * self.__diameter_stone) / (
                    .5 * self.__finger_size + self.__height_workpiece))

        beta = np.arccos(root_level(.5 * self.__finger_size + self.__height_workpiece, .5 * self.__distance) / (
                .5 * self.__finger_size + self.__height_workpiece)) + 2 * np.arccos(
            root_level(.5 * self.__finger_size + self.__height_workpiece, .5 * self.__diameter_stone) / (
                    .5 * self.__finger_size + self.__height_workpiece))

        for i in range(self.__current_num):
            coordinates['x'].append((.5 * self.__finger_size + self.__height_workpiece) * np.cos(alpha))
            coordinates['y'].append((.5 * self.__finger_size + self.__height_workpiece) * np.sin(alpha))
            alpha -= beta

        for i in range(len(coordinates['x'])):
            ax.add_artist(
                plt.Circle((coordinates['x'][i], coordinates['y'][i]),
                           .5 * self.__diameter_stone,
                           fill=True,
                           color='salmon',
                           linewidth=0))

        ax.add_artist(circle_inner)
        ax.add_artist(circle_outer)

        plt.show()

    def control(self):
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
        self.illustrate()

        print('Выберите дальнейшие действия (напр. введите «13» или «45»):\n',
              '1. Изменить высоту заготовки.\n',
              '2. Изменить диаметр камня.\n',
              '3. Изменить область посадки камней.\n',
              '4. Изменить количество камней.\n',
              '5. Изменить расстояние между камнями.\n',
              '6. Выход.\n', sep='')

        choose = None
        choose = input_check(choose, 'str',
                             'value in (1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 23, 24, 25, 34, 35, 45, 123, 124, 125, 134, 135,\
                              145, 234, 235, 245, 345, 1234, 1235, 1245, 1345, 2345, 12345)',
                             'Ввведите цифру:',
                             'Данные некорректны, повторите ввод.')

        if choose.find('6') == -1:

            if choose.find('1') != -1:
                self.__height_workpiece = input_check(self.__height_workpiece, 'float', 'value > 0',
                                                      'Введите высоту шинки:',
                                                      'Данные некорректны, повторите ввод.')

            if choose.find('2') != -1:
                while True:
                    try:
                        self.__diameter_stone = float(
                            (input('Введите диаметр камушка, который находится в промежутке от 0.5 до %f:'
                                   % (2 * (self.__height_workpiece - .8)))))
                        if (self.__diameter_stone >= .5) and (
                                self.__diameter_stone <= 2 * (self.__height_workpiece - .8)):
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print('Данные некорректны, повторите ввод.')

            if choose.find('3') != -1:
                print('Выберите область посадки камней:\n',
                      '1. Камни расположены на четверти кольца.\n',
                      '2. Камни расположены на половине кольца.\n',
                      '3. Камни расположены на 3/4 кольца.\n',
                      '4. Камни расположены по всей длине окружности.\n', sep='')

                self.__code = input_check(self.__code, 'int', 'value in (1, 2, 3, 4)',
                                          'Введите цифру, которая соответсвует вашему выбору:',
                                          'Данные некорректны, повторите ввод.')

            if choose.find('4') != -1:
                while True:
                    try:
                        self.__current_num = int(
                            (input('Введите новое количество камней, которое находится в промежутке от 1 до %d:'
                                   % self.num_limit())))
                        if (self.__current_num > 0) and (self.__current_num <= self.num_limit()):
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print('Данные некорректны, повторите ввод.')

            if choose.find('5') != -1:
                self.__distance = input_check(self.__distance, 'float', 'value >= .2',
                                              'Введите расстояние между камнями, минимально значение это \
                                              0.2 (Количество камней может измениться!):',
                                              'Данные некорректны, повторите ввод.')

            self.control()


print('Вас приветствует программа для математических расчетов в повседневных задачах ювелирного мастера.\n')

num = None

while True:
    print('Выберите цифру, которая соответсвует вашему выбору.\n',
          '1. Узнать длину заготовки (кольца).\n',
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

    elif num == 2:
        model = Wax()
        model.wax_mass()

    elif num == 3:
        model = Wire()
        print('Длина проволоки равна: %.3f\n' % model.length_limit())

    elif num == 4:
        model = Plate()
        print('Неизвестный 3-ий размер пластины: %.3f\n' % model.metric_unknown())
        print('3-ий размер - это высота, если были введены ширина и длина.\n')

    elif num in [1, 5]:
        model = Ring()
        if num == 1:
            model.workpiece_length()
        else:
            model.control()
