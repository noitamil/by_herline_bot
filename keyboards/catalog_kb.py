from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.products import PRODUCTS


def categories_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Футболки", callback_data="cat_tshirts")],
            [InlineKeyboardButton(text="Топы", callback_data="cat_tops")],
            [InlineKeyboardButton(text="Платья", callback_data="cat_dresses")],
        ]
    )


def products_by_category_kb(category: str) -> InlineKeyboardMarkup:
    buttons = []

    for product in PRODUCTS:
        if product["category"] == category:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=product["name"],
                        callback_data=f"product_{product['id']}"
                    )
                ]
            )

    buttons.append(
        [InlineKeyboardButton(text="← Назад к категориям", callback_data="back_to_categories")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_card_kb(product_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Купить", callback_data=f"buy_{product_id}")],
            [InlineKeyboardButton(text="← Назад", callback_data="back_to_catalog")]
        ]
    )