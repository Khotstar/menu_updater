import os

from psycopg2 import connect, sql


class DB:
    """
        Class deals with DB operations
    """

    def get_connection(self):
        """ Gets DB connection """

        try:
            connection = connect(user=os.getenv("DB_USER"),
                                  password=os.getenv("DB_PASSWORD"),
                                  host=os.getenv("DB_HOST"),
                                  port=os.getenv("DB_PORT"),
                                  database=os.getenv("DB_DATABASE"))
            return connection
        except Exception as e:
            print(f"Couldn't connect to database: {e}")

    def write(self, table_name, rows):
        """ Inserts rows(a data dict or an array of data dicts) to the given table

        Parameters
        ----------
        table_name : str
            name of the table
        rows: dict/list
            a dictionary or list of dictionaries
        """

        if type(rows) is dict:
            data = [rows]
        else:
            data = rows
        columns = list( data[0].keys())
        fields = ", ".join(columns)
        records_list_template = ','.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({fields}) VALUES {records_list_template}"
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, [tuple(d.values()) for d in data])
                connection.commit()
            except Exception as e:
                print(e)
            cursor.close()
            connection.close()


    def get(self, table_name, filter_conditions = None):
        """ Returns a list of rows as data dicts for the given filter condition.
            If no filter_conditions specified returns list all rows from table

        Parameters
        ----------
        table_name : str
            name of the table
        filter_conditions: dict
            filter conditions as dictionary
        Returns
        -------
        list
           list of rows as dictionary
        """

        result = []
        connection = self.get_connection()
        query = f"SELECT * FROM {table_name}"
        filter_query_arr = []
        filter_query = ""
        if filter_conditions:
            filter_query = " WHERE"
            for col in filter_conditions:
                filter_query_arr.append(f" {col} = %({col})s")
            filter_query += " AND".join(filter_query_arr)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query + filter_query, filter_conditions)
                columns = [x.name for x in cursor.description]
                for row in cursor:
                    row = dict(zip(columns, row))
                    result.append(row)
            except Exception as e:
                print(e)
            cursor.close()
            connection.close()
        return result

    def delete(self, table_name, filter_conditions):
        """ Deletes table rows based on the fileter conditions(dictionary)
            Returns False for empty filter_conditions.

        Parameters
        ----------
        table_name : str
            name of the table
        filter_conditions: dict
            filter conditions as dictionary
        Returns
        -------
        bool
           True if delete is successful else False
        """

        status = True
        connection = self.get_connection()
        query = f"DELETE FROM {table_name}"
        filter_query_arr = []
        filter_query = ""
        if filter_conditions:
            filter_query = " WHERE"
            for col in filter_conditions:
                filter_query_arr.append(f" {col} = %({col})s")
            filter_query += " AND".join(filter_query_arr)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query + filter_query, filter_conditions)
                connection.commit()
            except Exception as e:
                print(e)
                status = False
            cursor.close()
            connection.close()
        return status
