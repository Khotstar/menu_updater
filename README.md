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

# Flow Diagram

![Flow Diagram](/docs/process_doc.jpg)


# Entry Class
- [menu_import.py](https://github.com/Khotstar/menu_updater/blob/master/menu_import.py)

# Environment Variables
- FTP_SERVER = "xxx.xxx.x.xx"
- FTP_SERVER_USER_NAME = "xxxxxx"
- FTP_SERVER_PASSWORD = "xxxxxxxx"

- DB_USER ="xxxx"
- DB_PASSWORD = "xxxxx"
- DB_HOST = "xxx.xxx.xx.xx"
- DB_PORT = "xxxx"
- DB_DATABASE = "xxxxx"


# Menu.json structure
```
{
   "category":[
      {
         "name":"Appetizer"
      },
      {
         "name":"Entree"
      },
      {
         "name":"Dessert"
      }
   ],
   "item":[
      {
         "name":"French Fries",
         "category":"Appetizer"
      },
      {
         "name":"Onion Rings",
         "category":"Appetizer"
      },
      {
         "name":"Sandwich",
         "category":"Entree"
      },
      {
         "name":"Tacos",
         "category":"Entree"
      },
      {
         "name":"Ice Cream Sundae",
         "category":"Dessert"
      }
   ],
   "restaurant":"Joe's Grill"
}

```

# Assumptions
- Helper functions get_categories and get_items except an argument file_name not json, so reading the file each function call.
- As exiting item can be removed from the menu, so added deleting unavaliable menu items from category_items table
- Unavabliable category_items canb't be deactived(adding extra column active status in database), so delting those records.
