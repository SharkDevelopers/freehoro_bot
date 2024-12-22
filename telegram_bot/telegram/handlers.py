import random
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message


from aiogram_media_cache import MediaManager
from shared.storage import Database
from shared.storage.models import Chat, User
from shared.utils import TimeUtils
from provider import Provider

from .middlewares import logger_handler
from .sending_pushes import planing_push
from . import constants, keyboards

router = Router()


@router.message(Command("start"), F.chat.type == "private")
@logger_handler
async def handler_start(message: Message, db: Database, media_manager: MediaManager):
    if await db.get_user_by_id(message.from_user.id) is None:
        create_user = User(
            id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            created_at=TimeUtils(),
        )
        await db.create_user(create_user)
        planing_push(message.from_user.id, 0)
    await message.answer_photo(
        # photo=FSInputFile("data/assets/lune_horoscope.png"),
        photo=media_manager.get_file_id("lune_horoscope.png"),
        caption=constants.welcome_text,
        reply_markup=keyboards.start_mkrup(),
        parse_mode="html",
    )


@router.message(F.text == "👈Назад", F.chat.type == "private")
@logger_handler
async def handler_back_to_menu(message: Message, media_manager: MediaManager):
    await message.answer_photo(
        # photo=FSInputFile("data/assets/lune_horoscope.png"),
        photo=media_manager.get_file_id("lune_horoscope.png"),
        caption=constants.welcome_text,
        reply_markup=keyboards.start_mkrup(),
        parse_mode="html",
    )


@router.message(F.text == "📜Образовательное меню", F.chat.type == "private")
@logger_handler
async def get_astro_menu(message: Message):
    await message.answer(constants.study_text, reply_markup=keyboards.study_mrkup())


@router.message(
    lambda message: message.text
    in [*constants.study_menu_texts.keys(), "✨Астро-совет на день"],
    F.chat.type == "private",
)
@logger_handler
async def get_astro_study(message: Message, media_manager: MediaManager):
    if message.text == "✨Астро-совет на день":
        await message.answer_photo(
            # photo=FSInputFile("data/assets/astro_advice.jpg"),
            photo=media_manager.get_file_id("astro_advice.jpg"),
            caption=random.choice(constants.astro_advices),
            reply_markup=keyboards.to_menu_mrkup(),
        )
    elif message.text == "✨Что такое астрология?":
        await message.answer_photo(
            # photo=FSInputFile("data/assets/astrology_is.jpg"),
            photo=media_manager.get_file_id("astrology_is.jpg"),
            caption=constants.study_menu_texts[message.text],
            reply_markup=keyboards.to_menu_mrkup(),
        )
    else:
        await message.answer(
            constants.study_menu_texts[message.text],
            reply_markup=keyboards.to_menu_mrkup(),
        )


@router.message(
    lambda message: message.text
    in ["✨Получить бесплатный гороскоп", "🙏Получить бесплатный гороскоп"],
    F.chat.type == "private",
)
@logger_handler
async def handler_get_horoscope(
    message: Message, db: Database, media_manager: MediaManager
):
    user = await db.get_user_by_id(message.from_user.id)
    if user and not user.have_chat:
        new_chat = Chat(
            user_id=user.id,
            full_name=user.full_name,
            username=user.username,
        )
        if await db.create_chat(new_chat):
            await db.update_user(user.id, {"have_chat": True})
    await message.answer_photo(
        # photo=FSInputFile("data/assets/year_horoscope.png"),
        photo=media_manager.get_file_id("year_horoscope.png"),
        caption=random.choice(constants.random_texts_year),
        reply_markup=keyboards.to_menu_mrkup(False),
        parse_mode="html",
    )
    await message.answer(
        text=constants.horoscope(user.id),
        reply_markup=keyboards.to_menu_mrkup(back_btn=False),
        parse_mode="html",
    )


@router.message(F.text, F.chat.type == "private")
@logger_handler
async def handler_message(message: Message, db: Database):
    user = await db.get_user_by_id(message.from_user.id)
    if user.have_chat:
        await Provider.notify_new_message(user.id, message.message_id, message.text)
