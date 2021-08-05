from flask import Flask, render_template
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "1698850662:AAH5uh9R1tGiyC5i43yp1P-qeHmD0YJB3Qw"


bot = Bot(token=API_TOKEN, timeout=100)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.callback_query_handler(lambda callback_query: 'trex' == str(callback_query.game_short_name))
async def send_trex(callback_query: types.CallbackQuery):
    url = 'https://gamesbot-trex.herokuapp.com/index.html?id=' + str(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id, url=url)


@dp.callback_query_handler(lambda call: 'game trex' in call.data)
async def game_trex(call: types.CallbackQuery):
    await bot.send_game(call.from_user.id, game_short_name='trex')


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
    # insert your games here
    await message.answer('Hello there! Which game do you want to play?', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=100)
