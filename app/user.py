import asyncio
from tokenize import generate_tokens

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from app.generators import ai_generate

user_router = Router()

@user_router.message(CommandStart())
async def cmd_star_user(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(0.5)
    await message.answer('Привет')

# Роутер реагирует на любой текст ответом от ИИ
@user_router.message()
async def user_message(message: Message):
    response = await ai_generate(message.text)
    await message.answer(response, parse_mode='Markdown')