from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from models.user_data import UserData
from keyboards.inline_kb import (
    get_gender_keyboard, 
    get_fitness_level_keyboard,
    get_goals_keyboard,
    get_training_place_keyboard,
    get_training_time_keyboard
)

class UserForm(StatesGroup):
    age = State()
    gender = State()
    weight = State()
    height = State()
    fitness_level = State()
    medical_history = State()
    individual_features = State()
    goals = State()
    training_place = State()
    training_time = State()

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать в Нейрофит! 🤖\n\n"
        "Я помогу вам составить персонализированную программу тренировок и питания.\n"
        "Для начала давайте заполним вашу анкету.\n\n"
        "Введите ваш возраст:"
    )
    await state.set_state(UserForm.age)

@router.message(UserForm.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 10 or age > 100:
            await message.answer("Пожалуйста, введите реальный возраст (10-100 лет):")
            return
        await state.update_data(age=age)
        await message.answer(
            "Выберите ваш пол:",
            reply_markup=get_gender_keyboard()
        )
        await state.set_state(UserForm.gender)
    except ValueError:
        await message.answer("Пожалуйста, введите число:")

@router.callback_query(UserForm.gender, F.data.startswith("gender_"))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    gender = "Мужской" if callback.data == "gender_male" else "Женский"
    await state.update_data(gender=gender)
    await callback.message.edit_text(f"Пол: {gender}")
    await callback.message.answer("Введите ваш вес (в кг):")
    await state.set_state(UserForm.weight)
    await callback.answer()

@router.message(UserForm.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        if weight < 20 or weight > 300:
            await message.answer("Пожалуйста, введите реальный вес (20-300 кг):")
            return
        await state.update_data(weight=weight)
        await message.answer("Введите ваш рост (в см):")
        await state.set_state(UserForm.height)
    except ValueError:
        await message.answer("Пожалуйста, введите число:")

@router.message(UserForm.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text.replace(',', '.'))
        if height < 100 or height > 250:
            await message.answer("Пожалуйста, введите реальный рост (100-250 см):")
            return
        await state.update_data(height=height)
        await message.answer(
            "Выберите уровень физической подготовки:",
            reply_markup=get_fitness_level_keyboard()
        )
        await state.set_state(UserForm.fitness_level)
    except ValueError:
        await message.answer("Пожалуйста, введите число:")

@router.callback_query(UserForm.fitness_level, F.data.startswith("fitness_"))
async def process_fitness_level(callback: CallbackQuery, state: FSMContext):
    fitness_map = {
        "fitness_minimal": "Минимальный",
        "fitness_medium": "Средний", 
        "fitness_high": "Высокий"
    }
    fitness_level = fitness_map[callback.data]
    await state.update_data(fitness_level=fitness_level)
    await callback.message.edit_text(f"Уровень подготовки: {fitness_level}")
    await callback.message.answer(
        "Опишите ваш анамнез (диагнозы, заболевания, травмы):\n"
        "Если отсутствуют - напишите 'Нет'"
    )
    await state.set_state(UserForm.medical_history)
    await callback.answer()

@router.message(UserForm.medical_history)
async def process_medical_history(message: Message, state: FSMContext):
    await state.update_data(medical_history=message.text)
    await message.answer(
        "Опишите индивидуальные особенности организма "
        "(аллергии, непереносимости, пищевые предпочтения):\n"
        "Если отсутствуют - напишите 'Нет'"
    )
    await state.set_state(UserForm.individual_features)

@router.message(UserForm.individual_features)
async def process_individual_features(message: Message, state: FSMContext):
    await state.update_data(individual_features=message.text)
    await message.answer(
        "Выберите вашу цель:",
        reply_markup=get_goals_keyboard()
    )
    await state.set_state(UserForm.goals)

@router.callback_query(UserForm.goals, F.data.startswith("goal_"))
async def process_goals(callback: CallbackQuery, state: FSMContext):
    goals_map = {
        "goal_weight_loss": "Сброс веса",
        "goal_maintenance": "Поддержание веса", 
        "goal_weight_gain": "Набор веса",
        "goal_cutting": "Сушка",
        "goal_muscle_gain": "Набор мышечной массы"
    }
    goal = goals_map[callback.data]
    await state.update_data(goals=goal)
    await callback.message.edit_text(f"Цель: {goal}")
    await callback.message.answer(
        "Где планируете заниматься?",
        reply_markup=get_training_place_keyboard()
    )
    await state.set_state(UserForm.training_place)
    await callback.answer()

@router.callback_query(UserForm.training_place, F.data.startswith("place_"))
async def process_training_place(callback: CallbackQuery, state: FSMContext):
    place_map = {
        "place_home": "Дома",
        "place_gym": "В зале",
        "place_office": "В офисе",
        "place_outdoor": "На улице", 
        "place_none": "Не планирую"
    }
    place = place_map[callback.data]
    await state.update_data(training_place=place)
    await callback.message.edit_text(f"Место тренировок: {place}")
    await callback.message.answer(
        "Сколько времени готовы уделять тренировкам?",
        reply_markup=get_training_time_keyboard()
    )
    await state.set_state(UserForm.training_time)
    await callback.answer()

@router.callback_query(UserForm.training_time, F.data.startswith("time_"))
async def process_training_time(callback: CallbackQuery, state: FSMContext):
    time_map = {
        "time_1_2": "1-2 дня в неделю",
        "time_3_4": "3-4 дня в неделю",
        "time_5_6": "5-6 дней в неделю"
    }
    training_time = time_map[callback.data]
    await state.update_data(training_time=training_time)
    
    # Получаем все данные
    user_data = await state.get_data()
    
    # Формируем анкету
    questionnaire = format_questionnaire(user_data)
    
    await callback.message.edit_text(f"Время тренировок: {training_time}")
    await callback.message.answer(
        "🎉 Анкета заполнена! Вот ваши данные:\n\n" + questionnaire
    )
    
    await state.clear()
    await callback.answer()

def format_questionnaire(user_data: dict) -> str:
    return f"""
📋 Ваша анкета Нейрофит:

👤 Возраст: {user_data.get('age', 'Не указан')}
⚧ Пол: {user_data.get('gender', 'Не указан')}
⚖️ Вес: {user_data.get('weight', 'Не указан')} кг
📏 Рост: {user_data.get('height', 'Не указан')} см
💪 Уровень подготовки: {user_data.get('fitness_level', 'Не указан')}

🏥 Анамнез: {user_data.get('medical_history', 'Не указан')}
🍎 Особенности: {user_data.get('individual_features', 'Не указан')}
🎯 Цель: {user_data.get('goals', 'Не указан')}

🏋️ Место тренировок: {user_data.get('training_place', 'Не указан')}
⏰ Время: {user_data.get('training_time', 'Не указан')}

Спасибо за заполнение анкеты! В будущем здесь будет подключена нейросеть для генерации персонализированной программы.
"""