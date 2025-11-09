from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder




def kb_builder(text= str | list[str],
               callback= str | list[str],
               size= int | list[int],
               **kwargs
               ) -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    if isinstance(callback, str):
        callback = [callback]
    if isinstance(size, int):
        size = [size]

    [builder.button(text=tx, callback_data=cl)
    for tx, cl in zip(text, callback)]
    builder.adjust(*size)
    return builder.as_markup(**kwargs)
    


def get_settings(is_enabled: bool = False) -> InlineKeyboardMarkup:

    """
    is_enabled: bool — стан налаштування (True/False)
    """
    

    status_emoji = "🟢" if is_enabled else "🔴"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{status_emoji}",
                    callback_data=f"toggle_settings:{is_enabled}"
                )
            ],

            [
                InlineKeyboardButton(text="Back", callback_data="back")
            ]
        ]
    )
    return keyboard


about_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="About", url="https://telegra.ph/Encoder-Bot--%D0%86nstrukc%D1%96ya-koristuvacha-10-29")
        ]
    ]
)