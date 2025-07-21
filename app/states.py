from aiogram.fsm.state import State, StatesGroup

class Chat(StatesGroup):
    text = State()
    wait = State()

class RequstForm(StatesGroup):
    dates = State()
    comand1 = State()
    comand2 = State()
    inputSostav1 = State()
    inputSostav2 = State()
    noInputSostav2 = State()
    isComrade = State()
    isComrade_check = State()
    done = State()

    checkForm = State()
    formS = State()

