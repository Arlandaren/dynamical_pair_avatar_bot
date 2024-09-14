from aiogram.utils.keyboard import InlineKeyboardBuilder

def menu(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Начать", callback_data=f"start_{user_id}")

    return kb.as_markup()


