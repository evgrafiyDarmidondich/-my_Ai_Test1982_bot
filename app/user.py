import asyncio

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiohttp import request
from sqlalchemy.orm import defer


from app.cat.footboll import foot
from app.generators import ai_generate
import app.keyboards as kb
from app.states import RequstForm, Chat

user_router = Router()

@user_router.message(CommandStart())
async def cmd_star_user(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(0.5)
    await message.answer('Привет', reply_markup=kb.main)    #Выводим кнопку начать и сообщение привет
    # (Нужно будет добавить условия использования)

# FSM
# Роутер реагирует на текст "Чат"
@user_router.message(F.text == 'Начать')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(RequstForm.dates)   #Устанавливаем состояние ввода даты
    await message.answer('Введите дату матча', reply_markup=ReplyKeyboardRemove())

@user_router.message(RequstForm.dates)
async def chatting_data(message: Message, state: FSMContext):
    await state.update_data(dates=message.text)  #cохраняем дату
    await message.answer("Введите название команды хозяев")
    await state.set_state(RequstForm.comand1)   #Устанавливаем состояние ввода названия команды1


@user_router.message(RequstForm.comand1)
async def chatting_comand1(message: Message, state: FSMContext):
    await state.update_data(comand1=message.text)   #Сохраняем название команды1
    await message.answer("Введите название команды гостей")
    await state.set_state(RequstForm.comand2)   #Устанавливаем состояние ввода названия команды2

###################

@user_router.message(RequstForm.comand2)
async def chatting_comand2(message: Message, state: FSMContext):
    await state.update_data(comand2=message.text)   #Сохраняем название команды2
    await message.answer(f"Посмотреть стартовые составы можно на\n https://www.sports.ru/football/\n")
    await message.answer(f"Будите вводить стартовые составы команд", reply_markup=kb.isCheck)
    await state.set_state(RequstForm.inputSostav1)  #Устанавливаем состояние ввода первого состава


#####################################################################
######################################################################
@user_router.callback_query(F.data == 'yes_s')
async def input_sostav1(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите состав команды хозяев")
    await state.set_state(RequstForm.inputSostav2)  #Устанавливаем состояние ввода второго состава

@user_router.callback_query(F.data == 'no_s')
async def no_input_sostav(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Это товарищеский матч?", reply_markup=kb.isComrade)
    await state.set_state(RequstForm.isComrade_check)

@user_router.message(RequstForm.inputSostav2)
async def input_sostav2(message: Message, state: FSMContext):
    await state.update_data(sostav1=message.text)
    await message.answer("Введите состав команды гостей")
    await state.set_state(RequstForm.isComrade)     #Устанавливаем состояние ввода выбора типа матча

 # Инлайн ветвление товарищеский ли матч
 #################################################################################
@user_router.message(RequstForm.isComrade)
async def is_Comrade(message: Message, state: FSMContext):
    await state.update_data(sostav2=message.text)
    await message.answer("Это товарищеский матч?", reply_markup=kb.isComrade)
    await state.set_state(RequstForm.isComrade_check)
    datas = await state.get_data()
    print(datas)

@user_router.callback_query(F.data == 'yes')
async def is_comrade_yes(callback: CallbackQuery, state: FSMContext):
    await state.update_data(isComrade='Футбольный товарищеский матч')
    await state.set_state(RequstForm.checkForm)
    await callback.message.answer("Проверить форму", reply_markup=kb.checkForm)
    datas = await state.get_data()
    print(datas)

@user_router.callback_query(F.data == 'no')
async def is_comrade_yes(callback: CallbackQuery, state: FSMContext):
    await state.update_data(isComrade='Футбольный матч')
    await state.set_state(RequstForm.checkForm)
    await callback.message.answer("Отправить форму?", reply_markup=kb.checkForm)
    datas = await state.get_data()
    print(datas)

###############################################################################

# для прогноза с составом
#################################################################################

@user_router.callback_query(F.data == 'check_form')
async def form_s(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RequstForm.done)
    datas = await state.get_data()
    requests1 = (
        f"{datas["isComrade"]}: {datas['comand1']} - {datas['comand2']},\n "
        f"пройдет {datas['dates']}.")
    await callback.message.answer(requests1)
    await callback.message.answer("Ждите ответ!!!")

    if "sostav1" not in datas:
        requests2 = (f"{datas["isComrade"]}: {datas['comand1']} - {datas['comand2']},\n пройдет {datas['dates']}."
                     f"Кто победит в этом матче и скакой вероятностью?")
    else:
        requests2 = (
            f"{datas["isComrade"]}: {datas['comand1']} - {datas['comand2']},\n пройдет {datas['dates']}."
                    f"стартовый состав {datas['comand1']}: {datas['sostav1']},"
                    f"стартовый состав {datas['comand2']}: {datas['sostav2']},"
                    f"Кто победит в этом матче и скакой вероятностью?")

    print(requests2)
    response = await ai_generate(requests2)
    await callback.message.answer(response, reply_markup=kb.main)

#################################################################################



