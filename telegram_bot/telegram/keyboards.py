from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def start_mkrup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✨Получить бесплатный гороскоп")],
            [KeyboardButton(text="📜Образовательное меню")],
        ],
        resize_keyboard=True,
    )


def to_menu_mrkup(back_btn: bool = True):
    # Создаем клавиатуру с условной кнопкой "Назад"
    keyboard = [
        [KeyboardButton(text="📜Образовательное меню")],
    ]

    if back_btn:
        # Добавляем кнопку "Назад", если back_btn = True
        keyboard.append([KeyboardButton(text="👈Назад")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def study_mrkup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✨Что такое астрология?"),
                KeyboardButton(text="✨Гороскоп — что это?"),
            ],
            [
                KeyboardButton(text="✨Как появился первый гороскоп?"),
                KeyboardButton(text="✨Астро-совет на день"),
            ],
            [
                KeyboardButton(text="✨Что изучают в астрологии?"),
                KeyboardButton(text="✨Что такое 12 домов в астрологии?"),
            ],
            [
                KeyboardButton(text="✨Какой дом отвечает за работу?"),
                KeyboardButton(text="✨Какой дом отвечает за семью?"),
            ],
            [KeyboardButton(text="🙏Получить бесплатный гороскоп")],
        ],
        resize_keyboard=True,
    )
