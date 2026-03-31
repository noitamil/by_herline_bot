from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "by herline 🤍\n\n"
        "_бренд для тех, кто не вне рамок_\n\n"
        "здесь вы можете:\n"
        "- изучить наши айтемы\n"
        "- выбрать размер\n"
        " -оформить заказ\n\n"
        "дальше я:"
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu_kb())

@router.message(F.text == "хочу узнать про доставку и оплату!")
async def delivery_and_payment(message: Message) -> None:
    text = (
        "*доставка и оплата*\n\n"
        "После оформления заказа мы связываемсяь с вами для подтверждения деталей.\n\n"
        "Оплата: по согласованию после подтверждения заказа.\n"
        "Доставка: обсуждается индивидуально в зависимости от страны и города.\n\n"
        "Если у вас есть вопросы по доставке, напишите нам через кнопку *хочу связаться с вами!*."
    )

    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu_kb()
    )

@router.message(F.text == "хочу связаться с вами!")
async def contact_info(message: Message) -> None:
    text = (
        "*Связаться с нами*\n\n"
        "Если у вас есть вопросы по размеру, доставке или заказу, напишите мне:\n\n"
        "Telegram: @by_herline_shop\n"
        "Instagram: @by_herline"

    )

    await message.answer(
        text,
        reply_markup=main_menu_kb()
    )