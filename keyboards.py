import math

from telebot import types

import config


def areas_keyboard(areas, page):
    """Generates keyboards with areas."""

    keyboard = types.InlineKeyboardMarkup(row_width=5)

    pages = math.ceil(len(areas) / config.ON_PAGE)

    for num, area in enumerate(areas[config.ON_PAGE*page-config.ON_PAGE:config.ON_PAGE*page]):
        keyboard.add(types.InlineKeyboardButton(f'{num + 1 + config.ON_PAGE * (page - 1)}. {area}', callback_data = f'a_{area[:29]}_{page}'))

    begin_callback = f'areapage_1'
    back_callback = f'areapage_{page - 1}'
    forward_callback = f'areapage_{page + 1}'
    end_callback = f'areapage_{pages}'

    if page == 1:
        begin_callback = 'not_available'
        back_callback = 'not_available'
    elif page == pages:
        forward_callback = 'not_available'
        end_callback = 'not_available'
    
    if len(areas) > config.ON_PAGE:
        begin = types.InlineKeyboardButton('<<<', callback_data = begin_callback)
        back = types.InlineKeyboardButton('<-', callback_data = back_callback)
        page = types.InlineKeyboardButton(f'{page}/{pages}', callback_data = 'not_available')
        forward = types.InlineKeyboardButton('->', callback_data = forward_callback)
        end = types.InlineKeyboardButton('>>>', callback_data = end_callback)
        keyboard.add(begin, back, page, forward, end)
    
    keyboard.add(types.InlineKeyboardButton('👍 Готово', callback_data = f'done'))
    keyboard.add(types.InlineKeyboardButton('❌ Очистить все', callback_data = f'clear'))

    return keyboard


def categories_keyboard(area, categories, page, prev_page, subscriptions):
    """Generates keyboards with categories."""

    keyboard = types.InlineKeyboardMarkup(row_width=5)

    pages = math.ceil(len(categories) / config.ON_PAGE)

    for num, category in enumerate(categories[config.ON_PAGE*page-config.ON_PAGE:config.ON_PAGE*page]):
        if (area, category,) in subscriptions:
            keyboard.add(types.InlineKeyboardButton(f'✅ {num + 1 + config.ON_PAGE * (page - 1)}. {category}', callback_data = f'c_{category[:27]}_{page}_{prev_page}'))
        else:
            keyboard.add(types.InlineKeyboardButton(f'{num + 1 + config.ON_PAGE * (page - 1)}. {category}', callback_data = f'c_{category[:27]}_{page}_{prev_page}'))

    begin_callback = f'cp_1_{prev_page}_{area[:26]}'
    back_callback = f'cp_{page - 1}_{prev_page}_{area[:26]}'
    forward_callback = f'cp_{page + 1}_{prev_page}_{area[:26]}'
    end_callback = f'cp_{pages}_{prev_page}_{area[:26]}'

    if page == 1:
        begin_callback = 'not_available'
        back_callback = 'not_available'
    elif page == pages:
        forward_callback = 'not_available'
        end_callback = 'not_available'
    
    if len(categories) > config.ON_PAGE:
        begin = types.InlineKeyboardButton('<<<', callback_data = begin_callback)
        back = types.InlineKeyboardButton('<-', callback_data = back_callback)
        page = types.InlineKeyboardButton(f'{page}/{pages}', callback_data = 'not_available')
        forward = types.InlineKeyboardButton('->', callback_data = forward_callback)
        end = types.InlineKeyboardButton('>>>', callback_data = end_callback)
        keyboard.add(begin, back, page, forward, end)
    
    keyboard.add(types.InlineKeyboardButton('👍 Готово', callback_data = f'done'))
    keyboard.add(types.InlineKeyboardButton('❌ Очистить все', callback_data = f'clear'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_{prev_page}'))
    
    return keyboard


def subscribe_keyboard():
    """Generates keyboard to subscribe for a job."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Обновить информацию', callback_data = f'subscribe'))

    return keyboard


def check_keyboard():
    """Generates keyboard to subscribe for a job."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Начать использование!', callback_data = f'check'))

    return keyboard


def change_keyboard():
    """Generates keyboard to subscribe for a job."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Изменить подписки', callback_data = f'subscribe'))

    return keyboard