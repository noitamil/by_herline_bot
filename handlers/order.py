from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config import load_config
from keyboards.order_kb import confirm_order_kb, cancel_reply_kb
from keyboards.catalog_kb import product_card_kb
from keyboards.main_menu import main_menu_kb
from data.products import PRODUCTS
from states import OrderFlow

router = Router()
config = load_config()


def get_product_by_id(product_id: str):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


@router.callback_query(OrderFlow.choosing_size, F.data.startswith("size_"))
async def choose_size(callback: CallbackQuery, state: FSMContext) -> None:
    size = callback.data.replace("size_", "")

    await state.update_data(size=size)
    await state.set_state(OrderFlow.entering_first_name)

    await callback.message.answer(
        "Введите ваше *имя*:",
        parse_mode="Markdown",
        reply_markup=cancel_reply_kb()
    )
    await callback.answer()


@router.callback_query(OrderFlow.choosing_size, F.data == "back_to_product")
async def back_to_product(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    product_id = data.get("product_id")
    product = get_product_by_id(product_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    text = (
        f"*{product['name']}*\n\n"
        f"_Цена: {product['price']} рублей_\n\n"
        f"{product['description']}\n\n"
        f"Доступные размеры: {', '.join(product['sizes'])}"
    )

    await state.clear()

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=product_card_kb(product_id)
    )
    await callback.answer()


@router.message(F.text == "Отменить заказ")
async def cancel_order_by_text(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Заказ отменён.\n\nВы можете начать заново:",
        reply_markup=main_menu_kb()
    )


@router.message(OrderFlow.entering_first_name)
async def get_first_name(message: Message, state: FSMContext) -> None:
    first_name = message.text.strip()

    await state.update_data(first_name=first_name)
    await state.set_state(OrderFlow.entering_last_name)

    await message.answer("Введите вашу *фамилию*:", parse_mode="Markdown")


@router.message(OrderFlow.entering_last_name)
async def get_last_name(message: Message, state: FSMContext) -> None:
    last_name = message.text.strip()

    await state.update_data(last_name=last_name)
    await state.set_state(OrderFlow.entering_phone)

    await message.answer("Введите ваш *номер телефона*:", parse_mode="Markdown")


@router.message(OrderFlow.entering_phone)
async def get_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()

    if len(phone) < 7:
        await message.answer("Номер выглядит слишком коротким. Введите телефон ещё раз.")
        return

    await state.update_data(phone=phone)
    await state.set_state(OrderFlow.entering_contact)

    await message.answer(
        "Введите *email* или *@username* в Telegram для связи:",
        parse_mode="Markdown"
    )


@router.message(OrderFlow.entering_contact)
async def get_contact(message: Message, state: FSMContext) -> None:
    contact = message.text.strip()

    await state.update_data(contact=contact)
    await state.set_state(OrderFlow.confirming_order)

    data = await state.get_data()

    text = (
        "*Проверьте ваш заказ:*\n\n"
        f"Товар: *{data['product_name']}*\n"
        f"Размер: *{data['size']}*\n"
        f"Цена: *{data['price']} рублей*\n\n"
        f"Имя: {data['first_name']}\n"
        f"Фамилия: {data['last_name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Контакт: {data['contact']}"
    )

    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "Подтвердите заказ:",
        reply_markup=confirm_order_kb()
    )


@router.callback_query(OrderFlow.confirming_order, F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    user = callback.from_user
    username = f"@{user.username}" if user.username else "нет username"

    admin_text = (
        "*Новый заказ*\n\n"
        f"Товар: *{data['product_name']}*\n"
        f"Размер: *{data['size']}*\n"
        f"Цена: *{data['price']} рублей*\n\n"
        f"Имя: {data['first_name']}\n"
        f"Фамилия: {data['last_name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Контакт: {data['contact']}\n\n"
        f"Telegram ID: `{user.id}`\n"
        f"Username: {username}"
    )

    await callback.bot.send_message(
        chat_id=config.admin_id,
        text=admin_text,
        parse_mode="Markdown"
    )

    await callback.message.answer(
        "Спасибо 🤍 Ваш заказ принят! Мы свяжимся с вами в ближайшее время.",
        reply_markup=main_menu_kb()
    )
    await state.clear()
    await callback.answer()


@router.callback_query(OrderFlow.confirming_order, F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    await callback.message.answer(
        "Заказ отменён.\n\nВы можете начать заново:",
        reply_markup=main_menu_kb()
    )

    await callback.answer()