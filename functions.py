import sqlite3
import telebot
import gspread
import itertools
import threading

import keyboards
import config


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

service_acc = gspread.service_account(filename='service_account.json')
sheet = service_acc.open(config.SPREAD_NAME)
work_sheet = sheet.worksheet(config.LIST_NAME)


def is_in_database(user_id):
    """Checks if user already in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT COUNT(id) 
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0][0]
    
    cursor.close()
    database.close()

    return users


def add_user(user_id):
    """Adds a new user to database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''
        INSERT INTO users (user_id, subscription)
        VALUES (?, ?)
        ''', (user_id, "[]"))
        
    database.commit()
    cursor.close()
    database.close()


def add_new_job(job_info):
    """Adds new job to database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''
        INSERT INTO jobs (area, category)
        VALUES (?, ?)
        ''', job_info)
        
    database.commit()
    cursor.close()
    database.close()


def delete_job(category):
    """Deletes job from database"""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute("DELETE FROM jobs WHERE category=?", (category,))
        
    database.commit()
    cursor.close()
    database.close()


def select_all_jobs():
    """Extracts all jobs from database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    jobs_info = cursor.execute('SELECT area, category FROM jobs').fetchall()
    
    cursor.close()
    database.close()

    return jobs_info


def select_areas():
    """Select areas from database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    areas = cursor.execute('SELECT DISTINCT(area) FROM jobs').fetchall()
    
    cursor.close()
    database.close()

    if areas:
        areas = list(itertools.chain.from_iterable(areas))

    return areas


def select_categories(area):
    """Select categories by areas."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    categories = cursor.execute(f'SELECT DISTINCT(category) FROM jobs WHERE area LIKE "{area}%"').fetchall()
    
    cursor.close()
    database.close()

    if categories:
        categories = list(itertools.chain.from_iterable(categories))

    return categories


def select_all_categories():
    """Extracts all categories from database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    categories = cursor.execute('SELECT category FROM jobs').fetchall()
    
    cursor.close()
    database.close()

    if categories:
        categories = list(itertools.chain.from_iterable(categories))

    return categories


def is_area_in_database(area):
    """Checks if user already in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    areas = cursor.execute(f'''SELECT COUNT(id) 
                            FROM jobs 
                            WHERE area LIKE '{area}%'
                            ''').fetchall()[0][0]
    
    cursor.close()
    database.close()

    return areas


def is_category_in_database(category):
    """Checks if user already in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    categories = cursor.execute(f'''SELECT COUNT(id) 
                            FROM jobs 
                            WHERE category LIKE '{category}%'
                            ''').fetchall()[0][0]
    
    cursor.close()
    database.close()

    return categories


def select_info_by_category(category):
    """Selects area by category."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    info = cursor.execute(f'''SELECT area, category 
                            FROM jobs 
                            WHERE category LIKE '{category}%'
                            ''').fetchall()[0]
    
    cursor.close()
    database.close()

    return info


def select_users_by_category(subscription):
    """Selects users by category."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT user_id
                            FROM users 
                            WHERE subscription LIKE "%{subscription}')%"
                            ''').fetchall()
    
    cursor.close()
    database.close()

    if users:
        users = set(itertools.chain.from_iterable(users))

    return users


def select_users_by_area(area):
    """Selects users by area."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT user_id
                            FROM users 
                            WHERE subscription LIKE "%('{area}', %"
                            ''').fetchall()
    
    cursor.close()
    database.close()

    if users:
        users = set(itertools.chain.from_iterable(users))

    return users


def select_users_by_subscription(subscription):
    """Selects area by category."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT user_id, subscription
                            FROM users 
                            WHERE subscription LIKE "%{subscription}%"
                            ''').fetchall()
    
    cursor.close()
    database.close()

    return users


def update_subscriptions(user_id, subscription):
    """Updates users subscriptions."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET subscription=?
                    WHERE user_id=?
                    ''', (subscription, user_id,))

    database.commit()
    cursor.close()
    database.close()


def clear_database():
    """Updates users subscriptions."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute('DELETE FROM jobs')

    database.commit()
    cursor.close()
    database.close()


def select_full_area(area):
    """Select full area name."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    area = cursor.execute(f'SELECT area FROM jobs WHERE area LIKE "{area}%"').fetchall()[0][0]
    
    cursor.close()
    database.close()

    return area


def extract_subscriptions(user_id):
    """Extract's users subscriptions."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    subscription = cursor.execute(f'''SELECT subscription 
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0][0]
    
    cursor.close()
    database.close()

    return eval(subscription)


def validate_table(areas, categories):
    """Validates google spread if it format is ok to parse."""

    # вторая ячейка в категориях - пуста
    if categories[0] != '':
        return False
    
    # количество сфер совпадает с количеством пропусков в категориях
    elif len(areas) - areas.count('') != categories.count(''):
        return False

    # значения в сферах уникальны
    elif len(areas) - areas.count('') != len(set(areas)) - 1:
        return False

    # значения в категория уникальны
    elif len(categories) - categories.count('') != len(set(categories)) - 1:
        return False
    
    return True


def get_areas_values():
    """Gets jobs areas values from google spread."""

    return work_sheet.col_values(1)[1::]


def get_final_areas(areas):
    """Extract job's areas from values."""

    final_areas = []

    for area in areas:
        if area != '':
            final_areas.append(area)

    return final_areas


def get_categories_values():
    """Gets jobs categories values from google spread."""

    return work_sheet.col_values(2)[1::]


def get_final_categories(categories):
    """Extract job's categories from values."""

    pointer = -1
    categories_by_areas = []

    for category in categories:
        if category == '':
            categories_by_areas.append(list())
            pointer += 1
        else:
            categories_by_areas[pointer].append(category)

    return categories_by_areas


def sort_areas_categories(areas, categories_by_areas):
    """Sorts categories and areas."""

    jobs_provided = []

    for num, categories_by_area in enumerate(categories_by_areas):
        for category in categories_by_area:
            jobs_provided.append((areas[num], category,))

    return jobs_provided


def find_deleted_jobs(spread_jobs, database_jobs):
    """Finds jobs that where deleted from spread."""

    deleted_jobs = []

    for database_job in database_jobs:
        if database_job not in spread_jobs:
            deleted_jobs.append(database_job)
    
    return deleted_jobs


def find_added_jobs(spread_jobs, database_jobs):
    """Finds jobs that where added to spread."""

    added_jobs = []

    for spread_job in spread_jobs:
        if spread_job not in database_jobs:
            added_jobs.append(spread_job)
    
    return added_jobs


def from_spread_to_database():
    """Parses information from spread to database."""

    areas = get_areas_values()
    categories = get_categories_values()

    if validate_table(areas, categories):
        areas = get_final_areas(areas)
        categories = get_final_categories(categories)

        spread_jobs = sort_areas_categories(areas, categories)
        database_jobs = select_all_jobs()

        deleted_jobs = find_deleted_jobs(spread_jobs, database_jobs)
        added_jobs = find_added_jobs(spread_jobs, database_jobs)

        for deleted_job in deleted_jobs:
            delete_job(deleted_job[1])

        for added_job in added_jobs:
            add_new_job(added_job)

        threading.Thread(daemon=True, target=handle_unsubscribe, args=(deleted_jobs,)).start()
        threading.Thread(daemon=True, target=handle_new_categories, args=(added_jobs,)).start()

        reply_text = 'База данных успешно обновлена.'

    else:
        duplicated_categories = set()

        for category in categories:
            if categories.count(category) > 1 and category != '':
                duplicated_categories.add(category)

        if duplicated_categories:
            reply_text = 'База данных не обновлена. Задублированы категории:\n'

            for duplicated_category in duplicated_categories:
                reply_text += f'{duplicated_category}\n'
        
        else:
            reply_text = 'База данных не обновлена, проверьте google таблицы на соответствие формату.'

    return reply_text


def text_subscriptions(subscriptions):
    """Generates text based on subscriptions."""

    if subscriptions:
        subscriptions_text = 'Вы подписаны на следующие оповещения:\n'
        subscriptions_by_area = {}

        for subscription in subscriptions:
            subscriptions_by_area[subscription[0]] = []

        for subscription in subscriptions:
            subscriptions_by_area[subscription[0]].append(subscription[1])

        counter = 1
        for area, categories in subscriptions_by_area.items():
            subscriptions_text += f'\n*{counter}. {area}:*\n'
            counter += 1

            for category in categories:
                subscriptions_text += f'- {category}\n'
        
        subscriptions_text += '\nНажмите «👍 Готово», когда закончите выбирать категории.\n'
    
    else:
        subscriptions_text = ''
    
    return subscriptions_text


def handle_channel_message(text, message_id):
    """Handles messages from target channel."""

    categories = select_all_categories()

    users = []

    for category in categories:

        job_titles =  text.split('\n')[-1].split(' | ')
        for job_title in job_titles:
            
            if job_title == category:
                users += select_users_by_category(category)

    users = set(users)

    for user in users:
        try:
            bot.forward_message(chat_id=user,
                                from_chat_id=config.CHANNEL_ID,
                                message_id=message_id,
                                )
        except:
            pass


def handle_unsubscribe(deleted_jobs):
    """Handles situations when category that user follows is deleted."""

    for deleted_job in deleted_jobs:
        users_info = select_users_by_subscription(deleted_job)

        for user_info in users_info:
            new_subscription = eval(user_info[1])
            new_subscription.remove(deleted_job)

            if not new_subscription:
                new_subscription = []

            update_subscriptions(user_info[0], str(new_subscription))

            try:
                bot.send_message(chat_id=user_info[0],
                                 text=f'Категория *{deleted_job[1]}*, на которую вы были подписаны, была удалена. Подписка отменена.',
                                 reply_markup=keyboards.change_keyboard(),
                                 parse_mode='Markdown',
                                 )
            except:
                pass


def handle_new_categories(added_jobs):
    """Handles situations when new category added."""

    users = []
    areas_info = []

    for added_job in added_jobs:
        users += select_users_by_area(added_job[0])
        areas_info.append((select_users_by_area(added_job[0]), added_job[0],))

    users = set(users)

    users_areas = {}

    for user in users:
        users_areas[user] = set()

    for info in areas_info:
        for user in info[0]:
            users_areas[user].add(info[1])

    for user, areas in users_areas.items():

        areas_text = ''
        for area in areas:
            areas_text += f'- {area}\n'

        try:
            bot.send_message(chat_id=user,
                                text=f'В сферах, которыми вы интересуетесь, появились новые категории:\n\n{areas_text}',
                                reply_markup=keyboards.change_keyboard(),
                                )
        except:
            pass


def from_spread_to_database_add():
    """Parses information from spread to database."""

    areas = get_areas_values()
    categories = get_categories_values()

    if validate_table(areas, categories):
        areas = get_final_areas(areas)
        categories = get_final_categories(categories)

        spread_jobs = sort_areas_categories(areas, categories)
        database_jobs = select_all_jobs()

        deleted_jobs = find_deleted_jobs(spread_jobs, database_jobs)
        added_jobs = find_added_jobs(spread_jobs, database_jobs)

        for deleted_job in deleted_jobs:
            delete_job(deleted_job[1])

        for added_job in added_jobs:
            add_new_job(added_job)

        reply_text = 'База данных успешно обновлена.'

    else:
        duplicated_categories = set()

        for category in categories:
            if categories.count(category) > 1 and category != '':
                duplicated_categories.add(category)

        if duplicated_categories:
            reply_text = 'База данных не обновлена. Задублированы категории:\n'

            for duplicated_category in duplicated_categories:
                reply_text += f'{duplicated_category}\n'
        
        else:
            reply_text = 'База данных не обновлена, проверьте google таблицы на соответствие формату.'

    return reply_text


def text_subscriptions_by_command(subscriptions):
    """Generates text based on subscriptions."""

    if subscriptions:
        subscriptions_text = 'Вы подписаны на следующие оповещения:\n'
        subscriptions_by_area = {}

        for subscription in subscriptions:
            subscriptions_by_area[subscription[0]] = []

        for subscription in subscriptions:
            subscriptions_by_area[subscription[0]].append(subscription[1])

        counter = 1
        for area, categories in subscriptions_by_area.items():
            subscriptions_text += f'\n*{counter}. {area}:*\n'
            counter += 1

            for category in categories:
                subscriptions_text += f'- {category}\n'
    
    else:
        subscriptions_text = 'У вас пока нет оформленных подписок.'
    
    return subscriptions_text


def count_by_category(category):
    """Checks if user already in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT COUNT(id) 
                            FROM users 
                            WHERE subscription LIKE "%'{category}')%"
                            ''').fetchall()[0][0]
    
    cursor.close()
    database.close()

    return users


def count_users_by_categories(user_id):
    areas = get_areas_values()
    categories = get_categories_values()

    if validate_table(areas, categories):
        areas = get_final_areas(areas)
        categories = get_final_categories(categories)

        spread_jobs = sort_areas_categories(areas, categories)

        categories_by_areas = {}

        for job in spread_jobs:
            if job[0] not in categories_by_areas.keys():
                categories_by_areas[job[0]] = []
            categories_by_areas[job[0]].append(job[1])

        reply_text = ''

        for num, info in enumerate(categories_by_areas.items()):
            reply_text += f'\n*{num + 1}. {info[0]}:*\n'

            for category in info[1]:
                count_users = count_by_category(category)
                reply_text +=f'- {category} (подписано пользователей: *{count_users}*)\n'

            try:
                bot.send_message(chat_id=user_id,
                                text=reply_text,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            except:
                try:
                    reply_text = reply_text.replace('*', '')

                    bot.send_message(chat_id=user_id,
                                text=reply_text,
                                disable_notification=True,
                                )
                except:
                    pass
            
            reply_text = ''
        
        try:
            bot.send_message(chat_id=user_id,
                             text='Выгрузка завершена.',
                             )
        except:
            pass

    else:
        try:
            bot.send_message(chat_id=user_id,
                             text='Google таблица не соответствует формату.',
                             )
        except:
            pass




