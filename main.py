from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "1743359088:AAGwmbWk-yJo6mbtwGGGsuM0agdIlduJKQI"


bot = Bot(token=API_TOKEN, timeout=100)
dp = Dispatcher(bot, storage=MemoryStorage())


# Game trex starts
@dp.callback_query_handler(lambda callback_query: 'trex' == str(callback_query.game_short_name))
async def send_trex(callback_query: types.CallbackQuery):
    url = 'https://gamesbot-trex.herokuapp.com/index.html?id=' + str(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id, url=url)


@dp.callback_query_handler(lambda call: 'game trex' == str(call.data))
async def game_trex(call: types.CallbackQuery):
    await bot.send_game(call.from_user.id, game_short_name='trex')
# Game trex ends


# Game g2048 starts
@dp.callback_query_handler(lambda callback_query: 'g2048' == str(callback_query.game_short_name))
async def send_2048(callback_query: types.CallbackQuery):
    url = 'https://play2048.co/?id=' + str(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id, url=url)


@dp.callback_query_handler(lambda call: 'game g2048' == str(call.data))
async def game_2048(call: types.CallbackQuery):
    await bot.send_game(call.from_user.id, game_short_name='g2048')
# Game g2048 ends

@dp.message_handler(commands=['help'])
@dp.message_handler(lambda message: message.text == '/help')
async def help(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='start', callback_data='start callback'))
    await message.answer('This bot implements multiple JS games. Type /start or just click button below', reply_markup=kb)


@dp.message_handler(commands=['start'])
@dp.callback_query_handler(lambda call: 'start callback' in call.data)
@dp.message_handler(lambda message: message.text == '/start')
async def start(message: types.Message):
    if type(message) == types.CallbackQuery:
        message = message.message

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="T-Rex jumping game", callback_data='game trex'))
    kb.add(types.InlineKeyboardButton(text="2048", callback_data='game g2048'))
    # add new game buttons here
    await message.answer('Hello there! Which game do you want to play?', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=100)
