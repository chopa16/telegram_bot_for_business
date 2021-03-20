from aiogram.dispatcher.filters import Command
import keyboard
import states
from aiogram import types
from aiogram.dispatcher import FSMContext
import re
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, message
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from imgFiles import paths, catalog
from load_all import bot, dp, db
class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name, tel_number, address) " \
                                     "VALUES ($1, $2, $3, $4, $5) RETURNING (id, username)"
    EXTRACT_INFORMATION = "SELECT * FROM foto "

    ADD_BUY_THING = "INSERT INTO buy_thing(chat_id_user, id_foto, quantity, size)"\
                                        "VALUES($1, $2, $3, $4)"
    EXTRACT_FINISH = "SELECT w1.thing, w1.cost, w2.size, w2.quantity FROM foto w1, buy_thing w2 WHERE w2.id_foto=w1.id AND w2.chat_id_user = $1"

    async def add_new_user(self, chat_id, username, full_name, tel_number, address):

        args = chat_id, username, full_name, tel_number, address
        command = self.ADD_NEW_USER
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass
    async def extract_information(self):
        command = self.EXTRACT_INFORMATION
        foto_info = await self.pool.fetch(command)
        return foto_info

    async def add_buy_thing(self, chat_id_user, id_foto, quantity, size):
        command = self.ADD_BUY_THING
        args = chat_id_user, id_foto, quantity, size
        await self.pool.fetch(command, *args)

    async def extract_finish(self, id_user):
        command = self.EXTRACT_FINISH
        arg = id_user
        check = await self.pool.fetch(command, id_user)
        return check
db = DBCommands()
foto_info =[]
@dp.message_handler(Command("start"))
async def show_menu(message: Message):
    await message.answer("Добро пожаловать уважаемый покупатель!!!\n\n"
                         "чтобы сделать заказ\n введите НОМЕР вашего ТЕЛЕФОНА, чтобы мы могли связаться с Вами")
    await states.User_info.Q1.set()
@dp.message_handler(state=states.User_info.Q1)
async def buying_goods(message: types.Message, state: FSMContext):
    tel_number = message.text
    user = types.User.get_current()
    chat_id = user.id
    username = user.username
    full_name = user.full_name
    address = ''
    args = await db.add_new_user(chat_id, username, full_name, tel_number, address)
    await message.answer("Выберите товар из меню ниже", reply_markup=keyboard.btn)
    await state.finish()
@dp.callback_query_handler(text_contains="goods")
async def buying_goods(call: CallbackQuery):
    await call.message.answer("Выберите раздел",
                              reply_markup=keyboard.goods_keyboard)
@dp.callback_query_handler(text_contains=("for_little"))
async def buying_little(call: CallbackQuery):
    callback_data = call.data
    print(callback_data)
    print(type(callback_data))
    foto_info = await db.extract_information()
    for rows in foto_info:
        cost = int(rows["cost"])
        size = str(rows["size"])
        thing =rows["thing"]
        cloth = rows["cloth"]
        f = catalog + rows["name"]
        id = rows["id"]
        textlookfor = r"\w*мес\w*|\w*62\w*|\w*68\w*|\w*74\w*|\w*80\w*|\w*86\w*"
        allresults = re.findall(textlookfor, size)
        select_thing_btn = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="выбрать",
                                     callback_data=keyboard.select_thing_callback.new(item_name3="thing", id_thing=id))
            ]
        ])
        try:
            with open(f, 'rb') as photo:
                if len(allresults) > 0:
                    await call.message.answer_photo(photo=photo, caption=str(thing) + ' ' + str(cloth) + '\n стоимость:' + str(
                        cost) + 'сум, размеры: ' + str(size) + ' ', reply_markup=select_thing_btn)
        except FileNotFoundError:
            pass
@dp.callback_query_handler(text_contains=("for_middle"))
async def buying_little(call: CallbackQuery):
    foto_info = await db.extract_information()
    for rows in foto_info:
        cost = int(rows["cost"])
        size = str(rows["size"])
        thing =rows["thing"]
        cloth = rows["cloth"]
        f = catalog + rows["name"]
        id = rows["id"]
        s = size.find("мес")+size.find("56")+size.find("62")+size.find("68")+size.find("74")+size.find("80")+size.find("86")+size.find("92")+7
        if s<0:
            textlookfor = r"\w*лет\w*"
            allresults = re.findall(textlookfor, size)
            # allresults = size.find("мес")
            select_thing_btn = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="выбрать",
                                         callback_data=keyboard.select_thing_callback.new(item_name3="thing", id_thing=id))
                ]
            ])
            try:
                with open(f, 'rb') as photo:
                    if len(allresults) >= 0:
                        await call.message.answer_photo(photo=photo, caption=str(thing) + ' ' + str(cloth) + '\n стоимость:' + str(
                            cost) + 'сум, ' + str(size) + ' ', reply_markup=select_thing_btn)
            except FileNotFoundError:
                pass
@dp.callback_query_handler(text_contains="for_adult")
async def buying_adult(call: CallbackQuery):
    await call.message.answer("Пока нет товара для взрослых", reply_markup= keyboard.choiceBtn)

@dp.callback_query_handler(text_contains="all")
async def buying_adult(call: CallbackQuery):
    await call.message.answer("Пока нет товара для взрослых", reply_markup= keyboard.choiceBtn)
    foto_info = await db.extract_information()
    for rows in foto_info:
        cost = int(rows["cost"])
        size = str(rows["size"])
        thing = rows["thing"]
        cloth = rows["cloth"]
        f = catalog + rows["name"]
        id = rows["id"]
        select_thing_btn = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="выбрать",
                                     callback_data=keyboard.select_thing_callback.new(item_name3="thing", id_thing=id))
            ]
        ])
        try:
            with open(f, 'rb') as photo:
                await call.message.answer_photo(photo=photo,
                                                    caption=str(thing) + ' ' + str(cloth) + '\n стоимость:' + str(
                                                        cost) + 'сум, ' + str(size) + ' ',
                                                    reply_markup=select_thing_btn)
        except FileNotFoundError:
            pass
chosen_foto = []
@dp.callback_query_handler(text_contains="thing")
async def choose_size(call: CallbackQuery):


    callback_data = call.data
    id_foto = ""
    print(callback_data)
    for letter in callback_data:
        if letter.isnumeric():
            id_foto = id_foto+letter
    chosen_foto.append(int(id_foto))
    await call.message.reply("Напишите РАЗМЕР  выбранной вещи под этим сообщением")
    await states.ChosenThing.choose_size.set()
@dp.message_handler(state=states.ChosenThing.choose_size)
async def buying_goods(message: types.Message, state: FSMContext):
    print(chosen_foto)
    answer = message.text
    chosen_foto.append(answer) #размер под 1м индексом
    print(answer)
    await message.answer("Напишите количество выбранной вещи")
    state = dp.current_state(chat = message.chat.id, user=message.from_user.id)
    await states.ChosenThing.next()
@dp.message_handler(state=states.ChosenThing.choose_quantity)
async def answer_q1(message: types.Message, state: FSMContext):
    user = types.User.get_current()
    chat_id = user.id
    username = user.username
    full_name = user.full_name
    address = ''
    tel_number = ''
    args= await db.add_new_user(chat_id, username, full_name, tel_number, address)
    try:
        await db.add_buy_thing(chat_id, chosen_foto[0], int(message.text), chosen_foto[1])
    except ValueError:
        pass
    chosen_foto.pop(0)
    chosen_foto.pop(0)
    await message.answer("Отличный выбор!\n Для выбора еще товара нажмите ВЫБРАТЬ, который находится выше!!!", reply_markup=keyboard.choiceBtn)
    await state.finish()
@dp.callback_query_handler(text_contains="finish")
async def choose_size(call: CallbackQuery):
    user = types.User.get_current()
    chat_id = user.id
    callback_data = call.data
    check= await db.extract_finish(chat_id)
    print(check)
    text = ""
    for ch in check:
        t = ch["thing"]
        s = ch["size"]
        q = ch["quantity"]
        c = ch["cost"]
        text += f"""
{t} размер:{s}  кол-во:{q} стоимость{c}
            """
    await call.message.answer(text)
