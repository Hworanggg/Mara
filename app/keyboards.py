from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton

main=ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')


main_admin=ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассслыку')

catalog_list=InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Ethereum',callback_data='ETH'),
                 InlineKeyboardButton(text='Bitcoin', callback_data='BTC'),
                 InlineKeyboardButton(text='USDT',callback_data='USDT'))
cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')
