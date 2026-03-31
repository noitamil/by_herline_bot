from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def sizes_kb(sizes: list[str]) -> InlineKeyboardMarkup:
    buttons = []

    for size in sizes:
        buttons.append(
            [InlineKeyboardButton(text=size, callback_data=f"size_{size}")]
        )

    buttons.append(
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_product")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_order_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить заказ", callback_data="confirm_order")],
            [InlineKeyboardButton(text="Отменить", callback_data="cancel_order")],
        ]
    )


def cancel_reply_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отменить заказ")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )