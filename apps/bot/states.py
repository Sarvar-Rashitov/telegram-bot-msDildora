from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    """Foydalanuvchi ro'yxatdan o'tish jarayoni"""
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_phone = State()
    waiting_for_age = State()
    waiting_for_occupation = State()

class SupportTicketStates(StatesGroup):
    """Murojaat qoldirish jarayoni"""
    waiting_for_subject = State()
    waiting_for_message = State()
