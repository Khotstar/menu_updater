import json

from category import Category
from item import Item


class MenuHelper:
    """ Helper class for Menu"""

    def _read_json_file(self, file_name):
        """ Reads JSON file from local system

        Parameters
        ----------
        file_name : str
            json file name
        Returns
        -------
        json
            file content as JSON
        """
        with open(file_name, "r") as file_data:
            return json.loads(file_data.read())

    def get_categories(self, file_name):
        """Get Categories as list of dictionaries from json file

        Parameters
        ----------
        file_name : str
            json file name
        Returns
        -------
        list
           list of categories
        """
        json_file = self._read_json_file(file_name)
        category_list = []
        json_categories = json_file.get('category')
        for json_category in json_categories:
            name = json_category.get('name')
            category_list.append(Category(name))
        return category_list

    def get_items(self, file_name):
        """Get items as list of dictionaries from json file

        Parameters
        ----------
        file_name : str
            json file name
        Returns
        -------
        list
           list of items
        """
        json_file = self._read_json_file(file_name)
        item_list = []
        json_items = json_file.get('item')
        for json_item in json_items:
            name = json_item.get('name')
            category = json_item.get('category')
            item_list.append(Item(name, category))
        return item_list
