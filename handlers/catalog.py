from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from data.products import PRODUCTS
from keyboards.catalog_kb import categories_kb, products_by_category_kb, product_card_kb
from keyboards.order_kb import sizes_kb
from states import OrderFlow


router = Router()


def get_product_by_id(product_id: str):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


@router.message(F.text == "хочу познакомиться с айтемами!")
async def open_catalog(message: Message) -> None:
    await message.answer(
        "Каталог by herline\n\nВыберите категорию:",
        reply_markup=categories_kb()
    )


@router.callback_query(F.data.startswith("cat_"))
async def open_category(callback: CallbackQuery) -> None:
    category = callback.data.replace("cat_", "")

    category_titles = {
        "tshirts": "Футболки",
        "tops": "Топы",
        "dresses": "Платья",
    }

    await callback.message.edit_text(
        f"*{category_titles.get(category, 'Категория')}*\n\nВыберите товар:",
        parse_mode="Markdown",
        reply_markup=products_by_category_kb(category)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("product_"))
async def show_product_card(callback: CallbackQuery, state: FSMContext) -> None:
    product_id = callback.data.replace("product_", "")
    product = get_product_by_id(product_id)


    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    await state.update_data(product_id=product["id"])

    caption = (
        f"*{product['name']}*\n\n"
        f"_Цена: {product['price']} рублей_\n\n"
        f"{product['description']}\n\n"
        f"Доступные размеры: {', '.join(product['sizes'])}"
    )

    photo = FSInputFile(product["photo"])

    await callback.message.delete()

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=product_card_kb(product_id)
    )

    await callback.answer()

@router.callback_query(F.data == "← Назад")
async def back_to_categories(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Каталог by herline\n\nВыберите категорию:",
        reply_markup=categories_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await callback.message.answer(
        "*Каталог by herline*\n\nВыберите категорию:",
        parse_mode="Markdown",
        reply_markup=categories_kb()
    )

    await callback.answer()

@router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: CallbackQuery, state: FSMContext) -> None:
    product_id = callback.data.replace("buy_", "")
    product = get_product_by_id(product_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    await state.update_data(
        product_id=product["id"],
        product_name=product["name"],
        price=product["price"],
        sizes=product["sizes"],
    )
    await state.set_state(OrderFlow.choosing_size)

    await callback.message.delete()

    await callback.message.answer(
        f"*{product['name']}*\n\nВыберите размер:",
        parse_mode="Markdown",
        reply_markup=sizes_kb(product["sizes"])
    )

    await callback.answer()






