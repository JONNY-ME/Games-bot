import logging
from decouple import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import text
import aiogram.utils.markdown as md

from Games import NumberGame, XOGame


API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)


class NForm(StatesGroup):
    action = State()

class XOForm(StatesGroup):
    action = State()

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    if state.get_state() is not None:
        await state.finish()
    await message.reply("Hello, welcome to the bot!")



@dp.message_handler(commands=['number_game'], state='*')
async def cmd_number_game(message: types.Message, state: FSMContext):
    if state.get_state() is not None:
        await state.finish()
    num_game = NumberGame()
    async with state.proxy() as data:
        data['num_game'] = num_game
    await message.reply("Enter a guess: ")
    await NForm.action.set()


@dp.message_handler(lambda message: message.text not in ['start', 'number_game'], state=NForm.action)
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
            msg += md.code(num_game.get_formatted_guesses()) + "\nEnter your guess"
            try:
                await message.edit_text(msg, parse_mode=ParseMode.MARKDOWN)
            except:
                pass



@dp.message_handler(commands=['xo_game'], state="*")
async def cmd_xo_game(message: types.Message, state: FSMContext):
    if state.get_state() is not None:
        await state.finish()
    xo_game = XOGame()
    async with state.proxy() as data:
        data['xo_game'] = xo_game
    in_kbrd = []
    j = 0
    for i in xo_game.board:
        _t = []
        for x in i:
            _t.append(types.InlineKeyboardButton(text=str(x), callback_data="XO "+str(j)))
            j += 1
        in_kbrd.append(_t)
    markup = types.InlineKeyboardMarkup(inline_keyboard=in_kbrd)
    await message.reply("Enter a move: ", reply_markup=markup)
    await XOForm.action.set()



@dp.callback_query_handler(lambda call: call.data.startswith("XO"), state=XOForm.action)
async def process_xo_game(query: types.InlineQuery, state: FSMContext):
    async with state.proxy() as sdata:
        xo_game = sdata['xo_game']
        data = query.data.split()[1]
        result, mess = xo_game.next_move(data)
        if result == 1:
            await query.message.delete()
            msg = md.code(xo_game.get_formatted_board()) + "\n" + mess
            await bot.send_message(query.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
            await state.finish()
        else:
            if result == 0:
                mess = "Enter the next move"

            in_kbrd = []
            j = 0
            for i in xo_game.board:
                _t = []
                for x in i:
                    _t.append(types.InlineKeyboardButton(text=str(x), callback_data="XO "+str(j)))
                    j += 1
                in_kbrd.append(_t)
            markup = types.InlineKeyboardMarkup(inline_keyboard=in_kbrd)
            try:
                await query.message.edit_text(text=mess, reply_markup=markup)
            except:
                pass
            sdata['xo_game'] = xo_game



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)