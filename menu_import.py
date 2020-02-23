from datetime import datetime
import logging


from db import DB
from ftp_client import FtpClient
from menu_helper import MenuHelper


class MenuImport:
    """
        Class for importing menu from FTP server
    """

    def import_menu(self):
        """Imports menu to database from Menu.js (FTP server)"""

        logging.warning(f"Menu Import started:{datetime.now()}")
        file_name = "Menu.json"
        db = DB()
        menu_helper = MenuHelper()
        try:
            # Load Menu.json from FTP server
            self.load_menu(file_name)
            # Get Categories from file
            categories_from_file = menu_helper.get_categories(file_name)
            # Get items from file
            items_from_file = menu_helper.get_items(file_name)
            # Get category list from database
            categories_from_db = db.get('categories')
            # Get Items list from database
            items_from_db = db.get('items')
            # Get category items list from database
            category_items_from_db = db.get('category_items')
            # Populate categories in database from Menu.json
            self.populate_categories(categories_from_file, categories_from_db, db)
            # Populate items in database from Menu.json
            self.populate_items(items_from_file, items_from_db, db)
            # Populate category items in database from Menu.json
            self.populate_category_items(items_from_file, items_from_db, categories_from_db, category_items_from_db, db)
            # Delete inactive(not available in Menu.js) category items from database
            self.delete_category_items(items_from_file, items_from_db, categories_from_db, category_items_from_db, db)
        except Exception as e:
            logging.error(f"Error while importing menu{e}")
        logging.warning(f"Menu Import Completed:{datetime.now()}")

    def load_menu(self, file_name):
        """ Downloads  menu from FTP server to local system

        Parameters
        ----------
        file_name : str
            Menu file name
        """

        ftpClient = FtpClient()
        ftpClient.download_file_from_ftp_server(file_name)


    def populate_categories(self,categories_from_file, categories_from_db, db):
        """ Populates new categories in db from menu file

        Parameters
        ----------
        categories_from_file : list
            List of categories from menu file(Menu.json)
        categories_from_db : list
            List of existing categories from database
        db: DB
            DB instance
        """
        for category_from_file in categories_from_file:
            inserted_category = self.create_category(category_from_file, categories_from_db, db)
            if inserted_category:
                categories_from_db.append(inserted_category[0])


    def populate_items(self, items_from_file, items_from_db, db):
        """ Populates new items in db from menu file.

        Parameters
        ----------
        items_from_file : list
            List of items from menu file(Menu.json)
        items_from_db : list
            List of existing items from database
        db: DB
            DB instance
        """

        for item_from_file in items_from_file:
            inserted_item = self.create_item(item_from_file, items_from_db, db)
            if inserted_item:
                items_from_db.append(inserted_item[0])

    def populate_category_items(self, items_from_file, items_from_db, categories_from_db, category_items_from_db, db):
        """ Populates new category items in db from menu file.

        Parameters
        ----------
        items_from_file : list
            List of items from menu file(Menu.json)
        items_from_db : list
            List of existing items from database
        categories_from_db : list
            List of existing categories from database
        category_items_from_db : list
            List of existing category items from database
        db: DB
            DB instance
        """

        for item_from_file in items_from_file:
            inserted_category_item = self.create_category_item(item_from_file, items_from_db, categories_from_db, category_items_from_db, db)
            if inserted_category_item:
                category_items_from_db.append(inserted_category_item[0])

    def delete_category_items(self, items, items_from_db, categories_from_db, category_items_from_db, db):
        """ Deletes category items which are not active(not available in Menu.json)

        Parameters
        ----------
        items : list
            List of items from menu file(Menu.json)
        items_from_db : list
            List of existing items from database
        categories_from_db : list
            List of existing categories from database
        category_items_from_db : list
            List of existing category items from database
        db: DB
            DB instance
        """

        for category_item_from_db in category_items_from_db:
            category_id = category_item_from_db.get("category_id")
            item_id = category_item_from_db.get("item_id")
            matched_category = [c for c in categories_from_db if c['id'] == category_id]
            matched_item = [i for i in items_from_db if i['id'] == item_id]
            delete = True
            if matched_category and matched_item:
                category_name = matched_category[0]["name"]
                item_name = matched_item[0]["name"]
                matched_category_item = [i for i in items if i.name == item_name and i.category_name == category_name]
                if matched_category_item:
                    delete = False
            if delete:
                db.delete("category_items", {"id":category_item_from_db["id"]})


    def create_category(self, category, categories_from_db, db):
        """ Creates new Category in db

        Parameters
        ----------
        category : object
            Category object
        categories_from_db : list
            List of existing categories from database
        db: DB
            DB instance
        Returns
        -------
        list
            list of dictionary for last inserted category
            None if category already exists in database
        """

        if self._is_new_category(category, categories_from_db):
            db.write("categories",category.__dict__)
            return db.get("categories", {"name":category.name})


    def create_item(self, item, items_from_db, db):
        """ Creates new item in db

        Parameters
        ----------
        item : object
            Item object
        items_from_db : list
            List of existing items from database
        db: DB
            DB instance
        Returns
        -------
        list
            list of dictionary for last inserted Item
            None if item already exists in database
        """

        if self._is_new_item(item, items_from_db):
            item_keys =["name"]
            item_obj = {x:item.__dict__[x] for x in item_keys}
            db.write("items", item_obj)
            return db.get("items", {"name":item.name})


    def create_category_item(self, item, items_from_db, categories_from_db, category_items_from_db, db):
        """ Creates new Category item in db

        Parameters
        ----------
        item : object
            Item Object
        items_from_db : list
            List of existing items from database
        categories_from_db : list
            List of existing categories from database
        category_items_from_db : list
            List of existing category items from database
        db: DB
            DB instance
        Returns
        -------
        list
            list of dictionary for last inserted category item
            None if category item already exists in database
        """

        category_name = item.category_name
        item_name = item.name
        matched_category = [c for c in categories_from_db if c['name'] == category_name]
        matched_item = [i for i in items_from_db if i['name'] == item_name]
        category_id = matched_category[0].get("id")
        item_id = matched_item[0].get("id")
        matched_category_item = None
        if category_items_from_db:
            matched_category_item = [ci for ci in category_items_from_db if ci['item_id'] == item_id and ci['category_id'] == category_id]
        if not matched_category_item:
            db.write("category_items", {"category_id":category_id, "item_id": item_id})
            return db.get("category_items", {"category_id":category_id, "item_id": item_id})

    def _is_new_category(self, category, existing_categories):
        """ returns category already present in DB or not

        Parameters
        ----------
        category : object
            Category object
        existing_categories : list
            List of existing categories from database
        Returns
        -------
        boolean
            category already exists in database or not
        """

        category_name = category.name
        matched = [c for c in existing_categories if c['name'] == category_name]
        if matched:
            return False
        return True


    def _is_new_item(self, item, existing_items):
        """ returns item already present in DB or not

        Parameters
        ----------
        item : object
            Item object
        existing_items : list
            List of existing items from database
        Returns
        -------
        boolean
            Item already exists in database or not
        """

        item_name = item.name
        matched = [i for i in existing_items if i['name'] == item_name]
        if matched:
            return False
        return True


if __name__ == "__main__":
    menuImport = MenuImport()
    menuImport.import_menu()
