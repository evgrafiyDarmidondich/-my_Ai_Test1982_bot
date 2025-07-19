import asyncio

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

user_router = Router()

@user_router.message(CommandStart())
async def cmd_star_user(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(0.5)
    await message.answer('Привет')