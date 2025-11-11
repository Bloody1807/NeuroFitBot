from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_gender_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Мужской", callback_data="gender_male")
    keyboard.button(text="Женский", callback_data="gender_female")
    return keyboard.adjust(2).as_markup()

def get_fitness_level_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Минимальный", callback_data="fitness_minimal")
    keyboard.button(text="Средний", callback_data="fitness_medium")
    keyboard.button(text="Высокий", callback_data="fitness_high")
    return keyboard.adjust(1).as_markup()

def get_goals_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Сброс веса", callback_data="goal_weight_loss")
    keyboard.button(text="Поддержание веса", callback_data="goal_maintenance")
    keyboard.button(text="Набор веса", callback_data="goal_weight_gain")
    keyboard.button(text="Сушка", callback_data="goal_cutting")
    keyboard.button(text="Набор мышечной массы", callback_data="goal_muscle_gain")
    return keyboard.adjust(2).as_markup()

def get_training_place_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Дома", callback_data="place_home")
    keyboard.button(text="В зале", callback_data="place_gym")
    keyboard.button(text="В офисе", callback_data="place_office")
    keyboard.button(text="На улице", callback_data="place_outdoor")
    keyboard.button(text="Не планирую", callback_data="place_none")
    return keyboard.adjust(2).as_markup()

def get_training_time_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="1-2 дня в неделю", callback_data="time_1_2")
    keyboard.button(text="3-4 дня в неделю", callback_data="time_3_4")
    keyboard.button(text="5-6 дней в неделю", callback_data="time_5_6")
    return keyboard.adjust(1).as_markup()