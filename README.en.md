# Job subscriber
## Изменить язык: [Русский](README.md)
***
Telegram bot for subscribing to interesting vacancies published in the channel.
## [LIVE](https://t.me/nadomnik_subscription_bot)
## [DEMO](README.demo.md)
## Functionality:
1. Sends a notification when a vacancy of interest is posted
2. Allows the administrator to view subscription statistics
3. Notifies about new vacancies in the area of interest
4. Allows you to edit the list of professions based on google tables
5. Checks the subscription to the channel before allowing the use
## Commands:
**For convenience, it is recommended to add these commands to the side menu of the bot using [BotFather](https://t.me/BotFather).**
- menu - calls the menu
- subscriptions - displays a list of subscriptions

**Commands available only to the manager:**
- update - updates the list of areas and categories from google tables
- clear - clears the database
- add - transfers the list of areas and categories from google sheets (without sending notifications to users)

## Installation and use:
- Logging in case of an error is carried out in the file py_log.log
- Install dependencies:
```sh
pip install -r requirements.txt
```
- specify in the .env file:
   - Bot telegram token: **TELEGRAM_TOKEN**=TOKEN
   - Bot ID: **BOT_ID**=ID (first digits from bot token, before :)
   - Manager ID: **MANAGER_ID**=MANAGER_ID; will have the right to execute commands available to the manager (if there are several - specify separated by commas)
   > To determine the user ID, you need to send any message from the corresponding account to the next [bot] (https://t.me/getmyid_bot). Value contained in **Your user ID** - User ID
   - Channel ID: **CHANNEL_ID**=ID; the channel from which messages are being monitored and subscribed to
   - **SPREAD_NAME** - table name in google sheets where spheres and categories are located\
   - **LIST_NAME** - sheet name in the table
   - **ON_PAGE**=10 - number of objects displayed in the keyboard
- get file with credentials (connection parameters):\
https://console.cloud.google.com/ \
https://www.youtube.com/watch?v=bu5wXjz2KvU - instruction from 00:00 to 02:35\
Save the resulting file in the root of the project, with the name **service_account.json**
- provide service e-mail with access to the table (instruction in the video at the link above)
- run the project:
```sh
python3 main.py
```
## Recommendations for use:
- Column A should contain the names of spheres
- In column In category name
- The names of spheres and categories must be unique
- Information is filled in from the second line (headings are located on the first line)
- Opposite the name of the sphere should not be the name of the category