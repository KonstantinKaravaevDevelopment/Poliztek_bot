from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.filters.command import Command
import toml
import logging
import asyncio

# TODO add languages chosing
import languageRU as RU
import languageEN
import languagePL
import languageBY

with open('secrets.toml') as f:
    key = toml.loads(f.read())["key"]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=key)
dp = Dispatcher()


@dp.message(Command("start"))
@dp.message(Text("🏘 Домой"))
async def cmd_start(message: types.Message):
    kb = [
        [
            # TODO add buttons formatting
            types.KeyboardButton(text="📜 Статистика"),
            types.KeyboardButton(text="🎲 Случайный"),
            types.KeyboardButton(text="🏠 Города"),
            types.KeyboardButton(text="🔍"),
            types.KeyboardButton(text="🏻 Что писать?")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(RU.RuStartPhrases, reply_markup=keyboard)


@dp.message(Command("write"))
@dp.message(Text("🏻 Что писать?"))
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

    await message.reply(RU.RuWhatToWrite, reply_markup=keyboard)


@dp.message(Command("stats"))
@dp.message(Text("📜 Статистика"))
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

    await message.reply(RU.RUStats, reply_markup=keyboard,  parse_mode="MarkdownV2")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
