"""
The SQL Connector class for the InClubSIT Backend.
"""
import os

from dotenv import dotenv_values
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()


class SQLAdapter:
    _instance = None

    def __init__(self):
        """
        Initialises the SQL connection.
        """
        # Initialise the DB
        config = {
            **dotenv_values(".env"),
            **os.environ
        }
        try:
            if "SQL_PORT" in config:
                self.db = mysql.connector.connect(
                    user=config["SQL_USER"],
                    password=config["SQL_PASSWORD"],
                    host=config["SQL_HOST"],
                    database=config["SQL_DATABASE"],
                    port=config["SQL_PORT"]
                )
            else:
                self.db = mysql.connector.connect(
                    user=config["SQL_USER"],
                    password=config["SQL_PASSWORD"],
                    host=config["SQL_HOST"],
                    database=config["SQL_DATABASE"]
                )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(err)
                print("Something is wrong with your SQL username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(err)
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

        Example:
            >>> sql = SQLAdapter()
            >>> sql.query("SELECT * FROM Club WHERE ClubID = %s", (1,))
            >>> sql.query("INSERT INTO Club (ClubName, ClubCategoryID, ClubDescription) VALUES (%s, %s, %s), ("Test Club", 1, "This is a test club")")
        """
        try:
            cursor = self.db.cursor()
        except mysql.connector.errors.OperationalError:
            self.reconnect()
            cursor = self.db.cursor()
        self.db.start_transaction()
        data = []
        try:
            cursor.execute(query, params)
            data = cursor.fetchall()
        except mysql.connector.Error as err:
            self.db.rollback()
            raise err
        self.db.commit()
        cursor.close()
        return data

    def reconnect(self):
        """Attempts to reconnect to the SQL database.
        """
        config = {
            **dotenv_values(".env"),
            **os.environ
        }
        try:
            if "SQL_PORT" in config:
                self.db = mysql.connector.connect(
                    user=config["SQL_USER"],
                    password=config["SQL_PASSWORD"],
                    host=config["SQL_HOST"],
                    database=config["SQL_DATABASE"],
                    port=config["SQL_PORT"]
                )
            else:
                self.db = mysql.connector.connect(
                    user=config["SQL_USER"],
                    password=config["SQL_PASSWORD"],
                    host=config["SQL_HOST"],
                    database=config["SQL_DATABASE"]
                )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(err)
                print("Something is wrong with your SQL username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(err)
                print("Database does not exist")
            else:
                print(err)
        else:
            print("SQL connection successful")

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
