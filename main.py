import logging

import matplotlib.pyplot as plt
import numpy as np
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

CHOICE, LENGTH, MASS, WEIGHT, ELEMENT, WIRE_TYPE, METRIC_1, METRIC_2, FINGER_SIZE, HEIGHT_WORKPIECE, DIAMETER_STONE, DISTANCE, CODE = range(
    13)

TOKEN = '1442596050:AAHiVx9nFBxRFInX_3xDtmWoi2ic6SuevgM'

reply_keyboard = [["Пересчет массы восковки в массу металла"],
                  ["Пересчет массы в длину проволки разных сечений"],
                  ["Толщина пластины при заданных размерах"],
                  ["Узнать длину заготовки (кольца)"],
                  ["Визуализировать кольцо"]]

markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

wire_keyboard = [['Квадратное', 'Круглое']]
wire_markup = ReplyKeyboardMarkup(wire_keyboard, resize_keyboard=True, one_time_keyboard=True)

metal_data = {
    'metals': ['Серебро', 'Медь', 'Платина', 'Бронза', 'Латунь', 'Золото 375', 'Золото 585', 'Золото 750'],
    'weight_specific': [11, 8.93, 21.45, 8.9, 8.5, 11.5, 14, 17],
    'density': [10.36, 8.92, 21.45, 8.8, 8.6, 11.54, 13.6, 15.45]}

metal_markup = ReplyKeyboardMarkup(
    [[metal_data['metals'][i]] for i in range(len(metal_data['metals']))],
    resize_keyboard=True, one_time_keyboard=True)

code_keyboard = [['Четверть кольца'],
                 ['Половина кольца'],
                 ['3/4 кольца'],
                 ['Вся длина окружности']]

code_markup = ReplyKeyboardMarkup(code_keyboard, resize_keyboard=True, one_time_keyboard=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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
    def __init__(self, mass, element):
        self._mass = mass
        self._element = element


class Plate(Controller):
    def __init__(self, mass, element, metric_1, metric_2):
        super().__init__(mass, element)
        self._metric_1 = metric_1
        self._metric_2 = metric_2

    def metric_unknown(self, update, context):
        """
        Input:
            1. Два известных параметра будущей пластины из списка: (длина, ширина, высота)
            2. Масса пластины
        Output:
            1. 3-ий (неизвестный) размер пластины
        """
        update.message.reply_text("Незивестная размерность изделия = %f" % (self._mass / metal_data['density'][
            metal_data['metals'].index(self._element)] / self._metric_1 / self._metric_2))


class Wire(Plate):
    def __init__(self, mass, element, metric_1, metric_2, type):
        super().__init__(mass, element, metric_1, metric_2)
        self.__type = type

    def length_limit(self, update, context):
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
        if self.__type == wire_keyboard[0][0]:
            update.message.reply_text("Максимальная возможная длина для вашего квадратного сечения: %f" % (
                    (self._mass / metal_data['density'][metal_data['metals'].index(self._element)]) / (
                    self._metric_1 * self._metric_2)))
        else:
            update.message.reply_text("Максимальная возможная длина для вашего круглого сечения: %f" % (
                    (self._mass / metal_data['density'][metal_data['metals'].index(self._element)]) / (
                    np.pi * (self._metric_1 / 2) ** 2)))

    def metric_unknown(self):
        return super().metric_unknown()


class Wax:
    """
    Input:
        1. Вес восковки (мастер модели)
        2. Код металла для отливки изделия
    Output:
        1. Масса металла, требуемая на определенную восковку
    """

    def __init__(self, weight, element):
        self.__weight = weight
        self.__element = element

    def wax_mass(self, update, context):
        update.message.reply_text("Масса металла, требуемая на твою восковку: %.2f" % (
                self.__weight * metal_data['weight_specific'][metal_data['metals'].index(self.__element)]))


class Ring:
    def __init__(self, finger_size, height_workpiece, diameter_stone, distance, code):
        self.__finger_size = finger_size
        self.__height_workpiece = height_workpiece
        self.__diameter_stone = diameter_stone
        self.__distance = distance
        self.__code = code
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

    def illustrate(self, update, context):
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

        plt.savefig('plt.png')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('plt.png', 'rb'))


def model_data(user_data):
    record = list()

    for key, value in user_data.items():
        record.append('{} - {}'.format(key, value))

    return "\n".join(record).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        "Привет! Я создан для помощи ювелирам! "
        "Для начала выбери что хочешь сделать:", reply_markup=markup)
    return CHOICE


def choice(update, context):
    user_data = context.user_data
    category = 'Choice'
    text = update.message.text
    user_data[category] = text
    logger.info("Choice: %s", update.message.text)
    if update.message.text == reply_keyboard[4][0] or update.message.text == reply_keyboard[3][0]:
        update.message.reply_text("Введи размер кольца")
        return FINGER_SIZE
    elif update.message.text == reply_keyboard[0][0]:
        update.message.reply_text("Введите вес мастер модели")
        return WEIGHT
    else:
        update.message.reply_text("Введи массу заготовки")
        return MASS


def mass(update, context):
    text = update.message.text
    try:
        if float(text) > 0:
            user_data = context.user_data
            category = 'Mass'
            user_data[category] = text
            logger.info("Mass: %s", update.message.text)
            update.message.reply_text("Теперь выбери металл, в котором будет отливаться изделие",
                                      reply_markup=metal_markup)
            return ELEMENT
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число, "
                                  "которое больше 0")
        return MASS


def weight(update, context):
    text = update.message.text
    try:
        if float(text) > 0:
            user_data = context.user_data
            category = 'Weight'
            user_data[category] = text
            logger.info("Weight: %s", update.message.text)
            update.message.reply_text("Теперь выбери металл, в котором будет отливаться изделие",
                                      reply_markup=metal_markup)
            return ELEMENT
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число, "
                                  "которое больше 0")
        return WEIGHT


def element(update, context):
    text = update.message.text
    if text in [metal_data['metals'][i] for i in range(len(metal_data['metals']))]:
        user_data = context.user_data
        category = 'Element'
        user_data[category] = text
        logger.info("Element: %s", update.message.text)
        if user_data['Choice'] == reply_keyboard[1][0]:
            update.message.reply_text("Хорошо, а теперь укажи тип сечения", reply_markup=wire_markup)
            return WIRE_TYPE
        elif user_data['Choice'] == reply_keyboard[0][0]:
            model = Wax(float(user_data['Weight']), user_data['Element'])
            model.wax_mass(update, context)
        else:
            update.message.reply_text("Хорошо, а теперь введи первую известную размерность")
            return METRIC_1  # при WEIGHT пусть отсылает к вызову функции
    else:
        update.message.reply_text("Данные некорректны, повтори ввод", reply_markup=wire_markup)
        return ELEMENT


def wire_type(update, context):
    user_data = context.user_data
    category = 'Wire Type'
    text = update.message.text
    user_data[category] = text
    logger.info("Wire Type: %s", update.message.text)
    if user_data['Wire Type'] == wire_keyboard[0][0]:
        update.message.reply_text("Хорошо, а теперь введите первую известную размерность")
    else:
        update.message.reply_text("Ого! Круглое сечение, тогда введите диаметр заготовки")
    return METRIC_1


def metric_1(update, context):
    text = update.message.text
    try:
        if float(text) > 0:
            user_data = context.user_data
            category = 'Metric_1'
            user_data[category] = text
            logger.info("Metric_1: %s", update.message.text)
            if user_data['Wire Type'] == wire_keyboard[0][1]:
                model = Wire(float(user_data['Mass']), user_data['Element'],
                             float(user_data['Metric_1']), None, user_data['Wire Type'])
                model.length_limit(update, context)
            else:
                update.message.reply_text("Так-так-так, а как же вторая размерность?")
                return METRIC_2
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число, "
                                  "которое больше 0")
        return METRIC_1


def metric_2(update, context):
    text = update.message.text
    try:
        if float(text) > 0:
            user_data = context.user_data
            category = 'Metric_2'
            user_data[category] = text
            logger.info("Metric_2: %s", update.message.text)
            if user_data['Wire Type'] == wire_keyboard[1][0]:
                model = Wire(float(user_data['Mass']), user_data['Element'],
                             float(user_data['Metric_1']), float(user_data['Metric_2']), user_data['Wire Type'])
                model.length_limit(update, context)
            else:
                model = Plate(float(user_data['Mass']), user_data['Element'],
                              float(user_data['Metric_1']), float(user_data['Metric_2']))
                model.metric_unknown(update, context)
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число, "
                                  "которое больше 0")
        return METRIC_2


def finger_size(update, context):
    text = update.message.text
    try:
        if float(text) > 0:
            user_data = context.user_data
            category = 'Finger Size'
            user_data[category] = text
            logger.info("Finger Size: %s", update.message.text)
            update.message.reply_text("Теперь введите высоту шинки")
            return HEIGHT_WORKPIECE
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число, "
                                  "которое больше 0")
        return FINGER_SIZE


def height_workpiece(update, context):
    text = update.message.text
    try:
        if float(text) > 0:
            user_data = context.user_data
            category = 'Height Workpiece'
            user_data[category] = text
            logger.info("Height Workpiece: %s", update.message.text)
            update.message.reply_text("Прекрасно! Укажите диаметр камня для инкрустации. "
                                      "Значение должно находится в промежутке от 0.5 до %f" % (
                                              2 * (float(user_data['Height Workpiece']) - .8)))
            return DIAMETER_STONE
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число, "
                                  "которое больше 0")
        return HEIGHT_WORKPIECE


def diameter_stone(update, context):
    text = update.message.text
    user_data = context.user_data
    try:
        if .5 <= float(text) <= 2 * (float(user_data['Height Workpiece']) - .8):
            category = 'Diameter Stone'
            user_data[category] = text
            logger.info("Diameter Stone: %s", update.message.text)
            update.message.reply_text("Введи предпочитаемое расстояние между камнями. "
                                      "Минимально значение это 0.2 (Количество камней может измениться!)")
            return DISTANCE
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число "
                                  "находится в промежутке от 0.5 до %.2f" % (
                                          2 * (float(user_data['Height Workpiece']) - .8)))
        return DIAMETER_STONE


def distance(update, context):
    text = update.message.text
    try:
        if float(text) >= .2:
            user_data = context.user_data
            category = 'Distance'
            user_data[category] = text
            logger.info("Distance: %s", update.message.text)
            update.message.reply_text("В какой области будут посажены камни?", reply_markup=code_markup)
            return CODE
        else:
            raise ValueError
    except ValueError:
        update.message.reply_text("Данные некорректны, повтори ввод, убедившись, что введено число, "
                                  "которое больше 0.2")
        return DISTANCE


def code(update, context):
    text = update.message.text
    if text in [i[0] for i in code_keyboard]:
        user_data = context.user_data
        category = 'Code'
        user_data[category] = text
        logger.info("Code: %s", update.message.text)
        model = Ring(float(user_data['Finger Size']),
                     float(user_data['Height Workpiece']),
                     float(user_data['Diameter Stone']),
                     float(user_data['Distance']),
                     [i[0] for i in code_keyboard].index(user_data['Code'])+1)
        model.illustrate(update, context)
    else:
        update.message.reply_text("Непонятненька, повтори еще раз", reply_markup=code_markup)
        return CODE


def cancel(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s отменил выбор", user.first_name)
    update.message.reply_text('Пока-пока! :3',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOICE: [CommandHandler('start', start), MessageHandler(Filters.text, choice)],

            MASS: [CommandHandler('start', start), MessageHandler(Filters.text, mass)],

            WEIGHT: [CommandHandler('start', start), MessageHandler(Filters.text, weight)],

            ELEMENT: [CommandHandler('start', start), MessageHandler(Filters.text, element)],

            WIRE_TYPE: [CommandHandler('start', start), MessageHandler(Filters.text, wire_type)],

            METRIC_1: [CommandHandler('start', start), MessageHandler(Filters.text, metric_1)],

            METRIC_2: [CommandHandler('start', start), MessageHandler(Filters.text, metric_2)],

            FINGER_SIZE: [CommandHandler('start', start), MessageHandler(Filters.text, finger_size)],

            HEIGHT_WORKPIECE: [CommandHandler('start', start), MessageHandler(Filters.text, height_workpiece)],

            DIAMETER_STONE: [CommandHandler('start', start), MessageHandler(Filters.text, diameter_stone)],

            DISTANCE: [CommandHandler('start', start), MessageHandler(Filters.text, distance)],

            CODE: [CommandHandler('start', start), MessageHandler(Filters.text, code)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
