from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="хочу познакомиться с айтемами!")],
            [KeyboardButton(text="хочу узнать про доставку и оплату!")],
            [KeyboardButton(text="хочу связаться с вами!")],
        ],
        resize_keyboard=True,
    )