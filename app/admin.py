from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

admin_router = Router()

@admin_router.message(Command('admin'))
async def cmd_admin(message: Message):
    await message.answer('Привет админ')