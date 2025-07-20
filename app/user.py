import asyncio
from pyexpat.errors import messages

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import CommandStart


from app.generators import ai_generate
import app.keyboards as kb
from app.states import RequstForm, Chat

user_router = Router()

@user_router.message(CommandStart())
async def cmd_star_user(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(0.5)
    await message.answer('Привет', reply_markup=kb.main)

# FSM
# Роутер реагирует на текст "Чат"
@user_router.message(F.text == 'Начать')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(RequstForm.datas)
    await message.answer('Введите дату матча', reply_markup=ReplyKeyboardRemove())

@user_router.message(RequstForm.datas)
async def chatting_data(message: Message, state: FSMContext):
    await state.update_data(datas=message.text)
    await message.answer("Введите название команды хозяев")
    await state.set_state(RequstForm.comand1)

@user_router.message(RequstForm.comand1)
async def chatting_comand1(message: Message, state: FSMContext):
    await state.update_data(comand1=message.text)
    await state.set_state(RequstForm.comand2)
    await message.answer("Введите название команды гостей")

@user_router.message(RequstForm.comand2)
async def chatting_comand2(message: Message, state: FSMContext):
    await state.update_data(comand2=message.text)
    await state.set_state(RequstForm.isComrade)
    await message.answer("Ждите сейчас найду где посмотреть стартовый состав на матч")


    dates = await state.get_data()
    reqwests = (f"Где посмотреть стартовый состав команд для матча {dates["comand1"]} - {dates["comand2"]}"
                f"который пройдё {dates["datas"]}")
    responses = await ai_generate(reqwests)
    await message.answer(responses)
    await message.answer("Матч товарищеский?", reply_markup=kb.isComrade)

@user_router.callback_query(F.data == 'yes')
async def chatting_isComrade_yes(callback: CallbackQuery, state: FSMContext):
    await state.update_data(isComrade='товарищеский матч')
    await state.set_state(RequstForm.done)
    await callback.answer("Форма готова")
    await callback.message.answer("Проверить форму", reply_markup=kb.checkForm)

@user_router.callback_query(F.data == 'no')
async def chatting_isComrade(callback: CallbackQuery, state: FSMContext):
    await state.update_data(isComrade='матч')
    await state.set_state(RequstForm.done)
    await callback.answer("Форма готова")
    await callback.message.answer("Проверить форму", reply_markup=kb.checkForm)

@user_router.callback_query(F.data == 'check_form')
async def chatting_done(callback: CallbackQuery, state: FSMContext):
    await callback.answer("!!!ЖДИТЕ!!!")
    dates = await state.get_data()
    requests = (f"Футбольный {dates["isComrade"]} пройдёт: {dates["datas"]}, "
               f"команда хозяев: {dates["comand1"]}, гости: {dates["comand2"]},"
               f"Кто победит и с какой вероятностью?")
    await state.set_state(RequstForm.form)
    await callback.message.answer(requests, reply_markup=kb.buttonDone)
    response = await ai_generate(requests) ##############
    await state.clear()
    await callback.message.answer(response, reply_markup=kb.main)

@user_router.callback_query(F.data == 'request_form')
async def wait_wait(callback: CallbackQuery):
    await callback.answer("!!!ЖДИТЕ!!!")

    await callback.message.bot.send_chat_action(chat_id=callback.message.from_user.id, action=ChatAction.TYPING)

    await callback.message.answer("Подождите, для вас генерируется ответ")


