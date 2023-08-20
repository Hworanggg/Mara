from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import  MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os


storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен')

class NewOrder(StatesGroup):
    type=State()
    name=State()
    desc=State()
    price=State()
    photo=State()



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAMsZN4XAv2x8WbReZxozAYCUw8mbuwAAisMAAIiMFhLyETiWNKnYRQwBA')
    await message.answer(f'{message.from_user.first_name} Добро пожаловать!',
                         reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизировались как администратор',reply_markup=kb.main_admin)



@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')




@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Техническая поддержка: @khanalieev')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'В данный момент товаров нет в наличии!!!', reply_markup=kb.catalog_list)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста!!!')


@dp.message_handler(text='Админ панель')
async def cart(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ панель',reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю')


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer(f'Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю')


@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery,state: FSMContext):
    async with state.proxy() as data:
        data['type']= call.data
    await call.message.answer(f'Напишите название товара',reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo,state=NewOrder.photo)
async def add_item_photo (message:types.Message,state:FSMContext):
    await message.answer('Это не фотография')

@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.text
    await db.add_item(state)
    await message.answer('Товар успешно создан!',)




@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')


@dp.message_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'ETH':
        await bot.send_message(chat_id=callback_query.from_user.id, text = 'Вы выбрали Etherium')
    elif callback_query.data == 'BTC':
        await bot.send_message(chat_id=callback_query.from_user.id, text = 'Вы выбрали Bitcoin')
    elif callback_query.data == 'USDT':
        await bot.send_message(chat_id=callback_query.from_user.id, text = 'Вы выбрали USDT')



if __name__ == '__main__':
    executor.start_polling(dp,on_startup=on_startup,skip_updates=True)

