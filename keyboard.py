from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy", "item_name")

btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Товары", callback_data=buy_callback.new(item_name="goods"))
    ]
])

section_callback = CallbackData("section", "item_name1")

goods_keyboard = InlineKeyboardMarkup( inline_keyboard=[
    [
        InlineKeyboardButton(text="для детей c 1 мес до 2 лет", callback_data=section_callback.new(item_name1="for_little"))
    ],
    [
        InlineKeyboardButton(text="для  детей с 3 года до 14 лет", callback_data=section_callback.new(item_name1="for_middle"))
    ],
    [
        InlineKeyboardButton(text="для взрослых", callback_data=section_callback.new(item_name1="for_adult"))
    ],
    [
        InlineKeyboardButton(text="все товары", callback_data=section_callback.new(item_name1="all"))
    ]
])

choice_callback = CallbackData("choice", "item_name2")
choiceBtn= InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Завершить заказ", callback_data=choice_callback .new(item_name2="finish"))
    ]
])
quantity_thing_callback=CallbackData("quantity", "quantity_number")
quantity_thing_btn=InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Количество", callback_data=quantity_thing_callback.new(quantity_number="number"))
    ]
])
select_thing_callback = CallbackData("select", "item_name3", "id_thing")