import logging
from decouple import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from Games import NumberGame


API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
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
    # store the num_game in state proxy data
    async with state.proxy() as data:
        data['num_game'] = num_game
    await message.reply("Enter a guess: ")
    await Form.action.set()

@dp.message_handler(state=Form.action)
async def process_number_game(message: types.Message, state: FSMContext):
    num_game = await state.proxy.get_data('num_game')
    result, mess = num_game.guess(message.text)
    if result == 1:
        await message.reply("You won!")
        await state.finish()
    elif result == -1:
        await message.reply("You lost!")
        await state.finish()
    else:
        msg = ""
        if mess:
            msg += mess + "\n"
        msg += "Enter your guess"
        await message.reply(msg)
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)