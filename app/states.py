from aiogram.fsm.state import State, StatesGroup

class Chat(StatesGroup):
    text = State()
    wait = State()

class RequstForm(StatesGroup):
    datas = State()
    comand1 = State()
    comand2 = State()
    matchInfo = State()
    isComrade = State()
    done = State()
    form = State()
