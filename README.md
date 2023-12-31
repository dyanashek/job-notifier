# Job subscriber
## Change language: [English](README.en.md)
***
Телеграмм бот для подписки на интересующие вакансии, публикующиеся в канале.
## [LIVE](https://t.me/nadomnik_subscription_bot)
## [DEMO](README.demo.md)
## Функционал:
1. Присылает уведомление при публикации интересующей вакансии
2. Позволяет администратору посмотреть статистику подписок
3. Уведомляет о новых вакансиях, в сфере интересов
4. Позволяет редактировать список профессии на основании google таблиц
5. Проверяет подписку на канал прежде чем разрешить использование
## Команды:
**Для удобства рекомендуется добавить данные команды в боковое меню бота, используя [BotFather](https://t.me/BotFather).**
- menu - вызывает меню
- subscriptions - отображает список подписок

**Команды доступные только менеджеру:**
- update - обновляет список сфер и категорий из google таблиц
- clear - очищает базу данных
- add - переносит список сфер и категорий из google таблиц (без отправки уведомлений пользователям)

## Установка и использование:
- Логирование при ошибке ведется в файл py_log.log
- Установить зависимости:
```sh
pip install -r requirements.txt
```
- в файле .env указать:
  - Токен телеграмм бота: **TELEGRAM_TOKEN**=ТОКЕН
  - ID бота: **BOT_ID**=ID (первые цифры из токена бота, до :)
  - ID менеджера: **MANAGER_ID**=MANAGER_ID; будет иметь право на выполнение команд, доступных менеджеру (если несколько - указать через запятую)
  > Для определения ID пользователя нужно отправить следующему [боту](https://t.me/getmyid_bot) любое сообщение с соответствующего аккаунта. Значение, содержащееся в **Your user ID** - ID пользователя
  - ID канала: **CHANNEL_ID**=ID; канал, из которого отслеживаются сообщения и на который проверяется подписка
  - **SPREAD_NAME** - имя таблицы в google sheets, где расположены сферы и категории\
  - **LIST_NAME** - имя листа в таблице 
  - **ON_PAGE**=10 - количество объектов, отображающихся в клавиатуре
- получить файл c credentials (параметрами для подключения):\
https://console.cloud.google.com/ \
https://www.youtube.com/watch?v=bu5wXjz2KvU - инструкция с 00:00 по 02:35\
Полученный файл сохранить в корне проекта, с именем **service_account.json**
- предоставить сервисному e-mail доступ к таблице (инструкция в видео по ссылке выше)
- запустить проект:
```sh
python3 main.py
```
## Рекомендации по использованию:
- В столбце A должны располагаться названия сфер
- В столбец В название категорий
- Названия сфер и категорий должны быть уникальными
- Информация заполняется со второй строки (на первой расположены заголовки)
- Напротив названия сферы не должно располагаться название категории
