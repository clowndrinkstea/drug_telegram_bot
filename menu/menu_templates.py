from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from messages_text import add_new_drug_text, notification_list_text, to_main_page_text, drug_type_ml_text, \
    drug_type_count_text, drug_type_sachet_text, drug_type_dose_text

main_menu = [
    [KeyboardButton(text=add_new_drug_text, resize_keyboard=True)],
    [KeyboardButton(text=notification_list_text, resize_keyboard=True)],
]
main_menu = ReplyKeyboardMarkup(keyboard=main_menu)

only_to_main_menu = [
    [KeyboardButton(text=to_main_page_text, resize_keyboard=True)],
]
only_to_main_menu = ReplyKeyboardMarkup(keyboard=only_to_main_menu)

drug_type_menu = [
    [KeyboardButton(text=drug_type_ml_text, resize_keyboard=True)],
    [KeyboardButton(text=drug_type_count_text, resize_keyboard=True)],
    [KeyboardButton(text=drug_type_sachet_text, resize_keyboard=True)],
    [KeyboardButton(text=drug_type_dose_text, resize_keyboard=True)],
]
drug_type_menu = ReplyKeyboardMarkup(keyboard=drug_type_menu)
