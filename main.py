from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
import os


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


main=ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')


main_admin=ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассслыку')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAMsZN4XAv2x8WbReZxozAYCUw8mbuwAAisMAAIiMFhLyETiWNKnYRQwBA')
    await message.answer(f'{message.from_user.first_name} Добро пожаловать!',
                         reply_markup=main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизировались как администратор',reply_markup=main_admin)



@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')




@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Техническая поддержка: @khanalieev')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'В данный момент товаров нет в наличии!!!')


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста!!!')


@dp.message_handler(text='Админ панель')
async def cart(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ панель',reply_markup=admin_panel)
    else:
        await message.reply('Я тебя не понимаю')



@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')


if __name__ == '__main__':
    executor.start_polling(dp)
