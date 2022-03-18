import logging
from decouple import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import text
import aiogram.utils.markdown as md

from Games import NumberGame


API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)


class NForm(StatesGroup):
    action = State()


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Hello, welcome to the bot!")

@dp.message_handler(commands=['number_game'])
async def cmd_number_game(message: types.Message, state: FSMContext):
    num_game = NumberGame()
    async with state.proxy() as data:
        data['num_game'] = num_game
    await message.reply("Enter a guess: ")
    await NForm.action.set()

@dp.message_handler(state=NForm.action)
async def process_number_game(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        num_game = data['num_game']
        result, mess = num_game.guess(message.text)
        if result == 1:
            await message.reply("You won!")
            await bot.send_message(message.chat.id, "Enter /number_game to start a new game")
            await state.finish()
        elif result == -1:
            await message.reply(f"You lost! The number was {num_game.get_generated_number()}")
            await state.finish()
        else:
            msg = ""
            if mess:
                msg += "❌"+mess + "\n"
            msg += md.code(num_game.get_formatted_guesses())
            msg += "\nEnter your guess"

            await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)