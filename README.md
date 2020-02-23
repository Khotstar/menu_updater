# Menu Updater
Updates menu from FTP server to database

Steps for importing menu to database
- Load Menu.json from FTP server
- Get Categories from file
- Get items from file
- Get category list from database
- Get Items list from database
- Get category items list from database
- Populate categories in database from Menu.json
- Populate items in database from Menu.json
- Populate category in database items from Menu.json
- Delete inactive(not available in Menu.js) category items from database

# Entry Class
- menu_import.py

# Environment Variables
- FTP_SERVER = "xxx.xxx.x.xx"
- FTP_SERVER_USER_NAME = "xxxxxx"
- FTP_SERVER_PASSWORD = "xxxxxxxx"

- DB_USER ="xxxx"
- DB_PASSWORD = "xxxxx"
- DB_HOST = "xxx.xxx.xx.xx"
- DB_PORT = "xxxx"
- DB_DATABASE = "xxxxx"


