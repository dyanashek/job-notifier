import telebot
import logging
import threading

import config
import functions
import keyboards


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    '''Handles start command.'''

    user_id = message.from_user.id

    if not functions.is_in_database(user_id):
        functions.add_user(user_id)

    try:
        status = bot.get_chat_member(chat_id=config.CHANNEL_ID,
                        user_id=user_id,
                        )
        print(status.status)
        if status.status == 'member' or status.status == 'creator':
            subscribed = True
        else:
            subscribed = False

    except:
        subscribed = False

    if subscribed:
        areas = functions.select_areas()

        subscriptions = functions.extract_subscriptions(user_id)
        subscriptions_text = functions.text_subscriptions(subscriptions)

        bot.send_message(chat_id=message.chat.id,
                              text=f'{subscriptions_text}\nВыберите *сферу*, в которой ищете работу:',
                              reply_markup=keyboards.areas_keyboard(areas, 1),
                              parse_mode='Markdown',
                              )

    else:
        bot.send_message(chat_id=message.chat.id,
                              text='Для запуска бота подпишитесь на наш канал https://t.me/nadomnik_online.',
                              reply_markup=keyboards.check_keyboard(),
                              )
        

@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id)

    call_data = call.data.split('_')
    query = call_data[0]

    if query == 'a':
        area = call_data[1]
        prev_page = int(call_data[2])

        if functions.is_area_in_database(area):
            categories = functions.select_categories(area)
            area = functions.select_full_area(area)

            subscriptions = functions.extract_subscriptions(user_id)
            subscriptions_text = functions.text_subscriptions(subscriptions)

            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'{subscriptions_text}\nВыберите интересующие вас категории в сфере *{area}*:',
                                    parse_mode='Markdown',
                                    )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.categories_keyboard(area, categories, 1, prev_page, subscriptions),
                                            )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Информация устарела, воспользуйтесь кнопкой для обновления.',
                                    )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.subscribe_keyboard(),
                                            )
    
    elif query == 'c':
        category = call_data[1]
        page = int(call_data[2])
        prev_page = int(call_data[3])

        if functions.is_category_in_database(category):
            info = functions.select_info_by_category(category)
            categories = functions.select_categories(info[0])
            subscriptions = functions.extract_subscriptions(user_id)

            if info in subscriptions:
                subscriptions.remove(info)
            else:
                subscriptions.append(info)

            functions.update_subscriptions(user_id, str(subscriptions))
            subscriptions_text = functions.text_subscriptions(subscriptions)

            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'{subscriptions_text}\nВыберите интересующие вас категории  в сфере *{info[0]}*:',
                                    parse_mode='Markdown',
                                    )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.categories_keyboard(info[0], categories, page, prev_page, subscriptions),
                                            )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Информация устарела, воспользуйтесь кнопкой для обновления.',
                                    )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.subscribe_keyboard(),
                                            )

    elif query == 'areapage':
        page = int(call_data[1])

        areas = functions.select_areas()

        subscriptions = functions.extract_subscriptions(user_id)
        subscriptions_text = functions.text_subscriptions(subscriptions)

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=f'{subscriptions_text}\nВыберите *сферу*, в которой ищете работу:',
                              parse_mode='Markdown',
                              )
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.areas_keyboard(areas, page),
                                      )

    elif query == 'cp':
        page = int(call_data[1])
        prev_page = int(call_data[2])
        area = call_data[3]

        if functions.is_area_in_database(area):
            categories = functions.select_categories(area)
            area = functions.select_full_area(area)

            subscriptions = functions.extract_subscriptions(user_id)
            subscriptions_text = functions.text_subscriptions(subscriptions)
            
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'{subscriptions_text}\nВыберите интересующие вас категории в сфере *{area}*:',
                                    parse_mode='Markdown',
                                    )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.categories_keyboard(area, categories, page, prev_page, subscriptions),
                                            )
        else:
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Информация устарела, воспользуйтесь кнопкой для обновления.',
                                    )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.subscribe_keyboard(),
                                            )
    
    elif query == 'subscribe':
        areas = functions.select_areas()

        subscriptions = functions.extract_subscriptions(user_id)
        subscriptions_text = functions.text_subscriptions(subscriptions)

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=f'{subscriptions_text}\nВыберите *сферу*, в которой ищете работу:',
                              parse_mode='Markdown',
                              )

        bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=keyboards.areas_keyboard(areas, 1),
                                            )

    elif query == 'back':
        page = int(call_data[1])
        areas = functions.select_areas()

        subscriptions = functions.extract_subscriptions(user_id)
        subscriptions_text = functions.text_subscriptions(subscriptions)

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=f'{subscriptions_text}\nВыберите *сферу*, в которой ищете работу:',
                              parse_mode='Markdown',
                              )
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.areas_keyboard(areas, page),
                                      )
    
    elif query == 'check':
        try:
            status = bot.get_chat_member(chat_id=config.CHANNEL_ID,
                            user_id=user_id,
                            )
            print(status.status)
            if status.status == 'member' or status.status == 'creator':
                subscribed = True
            else:
                subscribed = False

        except:
            subscribed = False

        if subscribed:
            areas = functions.select_areas()

            subscriptions = functions.extract_subscriptions(user_id)
            subscriptions_text = functions.text_subscriptions(subscriptions)

            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=f'{subscriptions_text}\nВыберите *сферу*, в которой ищете работу:',
                                parse_mode='Markdown',
                                )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.areas_keyboard(areas, 1),
                                        )

    elif query == 'clear':
        functions.update_subscriptions(user_id, '[]')

        areas = functions.select_areas()

        subscriptions = functions.extract_subscriptions(user_id)
        subscriptions_text = functions.text_subscriptions(subscriptions)

        bot.edit_message_text(chat_id=chat_id,
                            message_id=message_id,
                            text=f'{subscriptions_text}\nВыберите *сферу*, в которой ищете работу:',
                            parse_mode='Markdown',
                            )
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=keyboards.areas_keyboard(areas, 1),
                                    )
        
    elif query == 'done':
        subscriptions = functions.extract_subscriptions(user_id)
        subscriptions_text = functions.text_subscriptions_by_command(subscriptions)

        bot.edit_message_text(chat_id=chat_id,
                            message_id=message_id,
                            text=subscriptions_text,
                            parse_mode='Markdown',
                            )
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=keyboards.change_keyboard(),
                                    )


@bot.message_handler(commands=['menu'])
def start_message(message):
    areas = functions.select_areas()

    subscriptions = functions.extract_subscriptions(message.from_user.id)
    subscriptions_text = functions.text_subscriptions(subscriptions)

    bot.send_message(chat_id=message.chat.id,
                            text=f'{subscriptions_text}\nВыберите *сферу*, в которой ищете работу:',
                            reply_markup=keyboards.areas_keyboard(areas, 1),
                            parse_mode='Markdown',
                            )
    

@bot.message_handler(commands=['subscriptions'])
def start_message(message):
    subscriptions = functions.extract_subscriptions(message.from_user.id)
    subscriptions_text = functions.text_subscriptions_by_command(subscriptions)

    bot.send_message(chat_id=message.chat.id,
                        text=subscriptions_text,
                        reply_markup=keyboards.change_keyboard(),
                        parse_mode='Markdown',
                        )


@bot.message_handler(commands=['update'])
def start_message(message):
    if str(message.from_user.id) in config.MANAGER_ID:
        reply_text = functions.from_spread_to_database()

        bot.send_message(chat_id=message.chat.id,
                         text=reply_text,
                         )
    
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Доступ запрещен',
                         )


@bot.message_handler(commands=['add'])
def start_message(message):
    if str(message.from_user.id) in config.MANAGER_ID:
        reply_text = functions.from_spread_to_database_add()

        bot.send_message(chat_id=message.chat.id,
                         text=reply_text,
                         )
    
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Доступ запрещен',
                         )


@bot.message_handler(commands=['clear'])
def start_message(message):
    if str(message.from_user.id) in config.MANAGER_ID:

        functions.clear_database()

        bot.send_message(chat_id=message.chat.id,
                         text='База данных успешно очищена.',
                         )
    
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Доступ запрещен',
                         )


@bot.message_handler(content_types=['text'])
@bot.channel_post_handler()
def channel_post(message):
    print(message.chat.id)
    threading.Thread(daemon=True, target=functions.handle_channel_message, args=(message.text, message.id,)).start()


if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass