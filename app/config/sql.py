"""
The SQL Connector class for the InClubSIT Backend.
"""
import asyncio
from typing import Union

from dotenv import dotenv_values
import mysql.connector
from mysql.connector import errorcode


class SQLAdapter:
    _instance = None

    def __init__(self):
        """
        Initialises the SQL connection.
        """
        # Initialise the DB
        config = dotenv_values(".env")
        try:
            self.db = mysql.connector.connect(
                user=config["SQL_USER"],
                password=config["SQL_PASSWORD"],
                host=config["SQL_HOST"],
                database=config["SQL_DATABASE"],
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your SQL username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("SQL connection successful")

    # If the class is already initialised, return the instance
    # basically a singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQLAdapter, cls).__new__(cls)
        return cls._instance

    def close_db(self):
        """
        Closes the SQL database connection.
        """
        self.db.close()

    def get(
        self,
        table: str,
        columns: Union[str, list] = "*",
        where: str = None,
        order_by: str = None,
        limit: int = None
    ) -> dict:
        """
        Fetches data from the SQL database. Dynamic arguments can be passed to fetch data
        from a specific collection, document or query.

        Args:
            table (str): The name of the table to fetch data from.
            columns (list): The columns to fetch data from.
            where (str): The where clause to filter data.
            order_by (str): The order by clause to order data.
            limit (int): The limit clause to limit data.

        Returns:
            dict: The data from the SQL database.
        """
        # Initialise the cursor
        cursor = self.db.cursor()

        # Check if the table exists
        cursor.execute("SHOW TABLES LIKE %s", (table, ))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Table {table} does not exist")

        # Check that the columns exist in the table
        if isinstance(columns, list) and columns != ["*"]:
            for column in columns:
                if column == "*":
                    raise SyntaxError("Cannot use * in list of columns")
                cursor.execute("SHOW COLUMNS FROM %s LIKE %s",
                               (table, column, ))
                result = cursor.fetchone()
                if not result:
                    raise IndexError(
                        f"Column {column} does not exist in table {table}")
        else:
            cursor.execute("SHOW COLUMNS FROM %s", (table, ))
            result = cursor.fetchall()
            if not result:
                raise IndexError(
                    f"Not all columns {columns} exist in table {table}")

        if order_by is not None:
            if order_by not in ["ASC", "DESC"]:
                raise ValueError(f"Order by {order_by} is not valid")

        # Build the query in the format:
        # SELECT [column,...]
        # FROM [table]
        # WHERE [where]
        # ORDER BY [order_by]
        # LIMIT [limit]

        query = """
        SELECT %s
        FROM %s
        %s
        %s
        %s
        """

        # Build the parameters
        params = []
        if isinstance(columns, str):
            params.append(columns)
        else:
            params.append(", ".join(columns))
        params.append(table)
        if where:
            params.append(f"WHERE {where}")
        else:
            params.append("")
        if order_by:
            params.append(f"ORDER BY {order_by}")
        else:
            params.append("")
        if limit:
            params.append(f"LIMIT {limit}")
        else:
            params.append("")

        params = tuple(params)

        # Execute the query
        cursor.execute(query, params)

        # Fetch the data
        data = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Return the data
        return data

    def query(
        self,
        query: str,
        params: tuple = None
    ) -> list:
        """Runs a query on the SQL database.

        Args:
            query (str): The query (as a prepared statement) to run.
            params (tuple, optional): Parameters for the prepared query statement. Defaults to None.

        Raises:
            err: Any errors that occur during the query.

        Returns:
            list: The rows returned from the query.
        """
        cursor = self.db.cursor()
        self.db.start_transaction()
        data = []
        try:
            cursor.execute(query, params)
        except mysql.connector.Error as err:
            self.db.rollback()
            raise err
        finally:
            self.db.commit()
            data = cursor.fetchall()
            cursor.close()
        return data

    def add(self, collection_path, data, document_id=None):
        """
        Adds a document to the SQL database.

        Args:


        Returns:
            None
        """
        raise NotImplementedError

    def update(self):
        """
        Updates a document in the SQL database dynamically. Dynamic arguments can be passed to update data

        Args:


        Returns:
            None
        """
        raise NotImplementedError

    def delete(self):
        """
        Deletes documents from the SQL database.

        Args:


        Returns:
            None
        """

        raise NotImplementedError

    # Add additional methods here
