import toml
import logging
import asyncio
import config

# TODO add languages choosing
import languageRU as RU
import languageRU
import languageEN
import languagePL
import languageBY
from Database import Database

# Import modules for Aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, WebAppInfo, \
    InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text, Command


class Finder(StatesGroup):
    input_data = State()


with open('secrets.toml', "r") as f:
    config = toml.loads(f.read())
    key = config["key"]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=key)
dp = Dispatcher(bot)
database = Database(config["api_key"], config["base_id"])


@dp.message_handler(Command("start"))
@dp.message_handler(Text("🏘 Домой"))
@dp.message_handler(Text("🏘 Домой"))
async def cmd_start(message: types.Message):
    kb = [
        [
            # TODO add buttons formatting
            types.KeyboardButton(text="📜 Статистика"),
            types.KeyboardButton(text="🎲 Случайный"),
            types.KeyboardButton(text="🏠 Города"),
            types.KeyboardButton(text="🔍"),
            types.KeyboardButton(text="🏻 Что писать?"),
            types.KeyboardButton(text="Задонатить")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.answer(RU.RuStartPhrases, reply_markup=keyboard)


# choose currency keyboard
b1_RU = KeyboardButton(languageRU.bt_1_kw_wal)
b2_RU = KeyboardButton(languageRU.bt_2_kw_wal)
b3_RU = KeyboardButton(languageRU.bt_3_kw_wal)
b4_RU = KeyboardButton(languageRU.bt_4_kw_wal)
currency_keybord = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True чтоб прятать клавиатуру
currency_keybord.add(b1_RU).insert(b2_RU).add(b4_RU).insert(b3_RU)

b1_RU = KeyboardButton(languageRU.bt_1_kw_wal_EU)
b2_RU = KeyboardButton(languageRU.bt_2_kw_wal_EU)
b3_RU = KeyboardButton(languageRU.bt_3_kw_wal_EU)
b4_RU = KeyboardButton(languageRU.bt_4_kw_wal_EU)
currency_keybord_EU = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True чтоб прятать клавиатуру
currency_keybord_EU.add(b1_RU).insert(b2_RU).add(b4_RU).insert(b3_RU)

b1_RU = KeyboardButton(languageRU.bt_1_kw_wal_US)
b2_RU = KeyboardButton(languageRU.bt_2_kw_wal_US)
b3_RU = KeyboardButton(languageRU.bt_3_kw_wal_US)
b4_RU = KeyboardButton(languageRU.bt_4_kw_wal_US)
currency_keybord_US = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True чтоб прятать клавиатуру
currency_keybord_US.add(b1_RU).insert(b2_RU).add(b4_RU).insert(b3_RU)

b1_RU = KeyboardButton(languageRU.bt_1_kw_wal_PL)
b2_RU = KeyboardButton(languageRU.bt_2_kw_wal_PL)
b3_RU = KeyboardButton(languageRU.bt_3_kw_wal_PL)
b4_RU = KeyboardButton(languageRU.bt_4_kw_wal_PL)
currency_keybord_PL = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True чтоб прятать клавиатуру
currency_keybord_PL.add(b1_RU).insert(b2_RU).add(b4_RU).insert(b3_RU)

b1_RU = KeyboardButton(languageRU.bt_4_kw_wal)
currency_keybord_back = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True чтоб прятать клавиатуру
currency_keybord_back.add(b1_RU)


@dp.message_handler(Command("write"))
@dp.message_handler(Text("🏻 Что писать?"))
async def what_write(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="🏘 Домой")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.reply(RU.RuWhatToWrite,
                        reply_markup=keyboard)


@dp.message_handler(Command("stats"))
@dp.message_handler(Text("📜 Статистика"))
async def stats(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="🏘 Домой")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer("Секундочку, сейчас посчитаем",
                         reply_markup=keyboard, parse_mode="MarkdownV2")
    answer = database.statistic()
    await message.answer(RU.RUStats.format(answer["prisoners_count"], answer["friends_count"], answer["tasks"],
                                           *[
                                               f"{len(i['fields']['userToPrisoner']) if 'userToPrisoner' in i['fields'] else 0} друзей {i['fields']['name']} /info@{i['fields']['shortName']}"
                                               for i in
                                               answer["less_friends"]]),
                         reply_markup=keyboard, parse_mode="MarkdownV2")


@dp.message_handler(Text(equals=languageRU.bt_4_kw_wal, ignore_case=True))
async def lests_go(message: types.Message):
    await bot.send_message(message.from_user.id, languageRU.go_back_to_main_menu, reply_markup=currency_keybord,
                           parse_mode="Markdown")


# Go back
@dp.message_handler(Text(equals=languageRU.bt_4_kw_wal_EU, ignore_case=True))
async def lests_go(message: types.Message):
    await bot.send_message(message.from_user.id, languageRU.go_back_to_main_menu, reply_markup=currency_keybord,
                           parse_mode="Markdown")


# EU
@dp.message_handler(Text(equals=languageRU.bt_1_kw_wal, ignore_case=True))
async def lests_go(message: types.Message):
    await bot.send_message(message.from_user.id, languageRU.how_much_money, reply_markup=currency_keybord_EU,
                           parse_mode="Markdown")


# US
@dp.message_handler(Text(equals=languageRU.bt_2_kw_wal, ignore_case=True))
async def lests_go(message: types.Message):
    await bot.send_message(message.from_user.id, languageRU.how_much_money, reply_markup=currency_keybord_US,
                           parse_mode="Markdown")


# PL
@dp.message_handler(Text(equals=languageRU.bt_3_kw_wal, ignore_case=True))
async def lests_go(message: types.Message):
    await bot.send_message(message.from_user.id, languageRU.how_much_money, reply_markup=currency_keybord_PL,
                           parse_mode="Markdown")


@dp.message_handler(Text("Задонатить"))
async def start_pay(message: types.Message):
    await bot.send_message(message.from_user.id, languageRU.RuFirstFraze, parse_mode="Markdown", reply_markup=currency_keybord)


@dp.message_handler(Command("find"))
@dp.message_handler(Text("🔍"))
async def find(message: types.Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text="🏘 Домой")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(
        text=RU.RuFind,
        reply_markup=keyboard
    )
    await state.set_state(Finder.input_data)


@dp.message_handler(Command("city"))
@dp.message_handler(Text("🏠 Города"))
async def city(message: types.Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text="🏘 Домой")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    prisoners_to_city = database.get_prisoners_by_city()
    await message.answer(
        text=RU.RuCity,
        reply_markup=keyboard
    )
    await state.set_state(Finder.input_data)




@dp.message_handler(Text(equals=languageRU.bt_1_kw_wal_EU, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_2_kw_wal_EU, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_3_kw_wal_EU, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_1_kw_wal_US, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_2_kw_wal_US, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_3_kw_wal_US, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_1_kw_wal_PL, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_2_kw_wal_PL, ignore_case=True), state='*')
@dp.message_handler(Text(equals=languageRU.bt_3_kw_wal_PL, ignore_case=True), state='*')
async def buy(message: types.Message, state: FSMContext):
    PAYMENT_TOKEN = ''
    if config.PAYMENTS_TOKEN_STRIPE_TEST.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, languageRU.info_for_users, reply_markup=currency_keybord_back,
                               parse_mode="Markdown")
        PAYMENT_TOKEN = config.PAYMENTS_TOKEN_STRIPE_TEST

    # Define image
    PHOTO_URL = 'https://focus.ua/static/storage/originals/8/52/65cda35bcf74cf80f0f0384bdf483528.jpg'
    MESSAGE_PAYMENT = 'Для политзаключенных 🤍❤️🤍'

    # Wybór waluty
    if message.text == languageRU.bt_1_kw_wal_EU:
        CURRENCY = languageRU.currency_EU
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=1000)
    elif message.text == languageRU.bt_2_kw_wal_EU:
        CURRENCY = languageRU.currency_EU
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=5000)
    elif message.text == languageRU.bt_3_kw_wal_EU:
        CURRENCY = languageRU.currency_EU
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=10000)
    elif message.text == languageRU.bt_1_kw_wal_US:
        CURRENCY = languageRU.currency_US
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=1000)
    elif message.text == languageRU.bt_2_kw_wal_US:
        CURRENCY = languageRU.currency_US
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=5000)
    elif message.text == languageRU.bt_3_kw_wal_US:
        CURRENCY = languageRU.currency_US
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=10000)
    elif message.text == languageRU.bt_1_kw_wal_PL:
        CURRENCY = languageRU.currency_PL
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=1000)
    elif message.text == languageRU.bt_2_kw_wal_PL:
        CURRENCY = languageRU.currency_PL
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=5000)
    elif message.text == languageRU.bt_3_kw_wal_PL:
        CURRENCY = languageRU.currency_PL
        PRICE = types.LabeledPrice(label=MESSAGE_PAYMENT, amount=10000)

    await bot.send_invoice(message.chat.id,
                           title=MESSAGE_PAYMENT,
                           description=MESSAGE_PAYMENT,
                           provider_token=PAYMENT_TOKEN,
                           currency=CURRENCY,
                           photo_url=PHOTO_URL,
                           photo_width=512,
                           photo_height=512,
                           photo_size=512,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter='denejki',
                           payload='text_invoice_payload')


# pre checkout
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_chekout_query(pre_chekout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_chekout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state: FSMContext):
    print('SUCCESSFUL PAYMENT: ')
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")


###################################################### Start bot ##################################################

# run long polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
