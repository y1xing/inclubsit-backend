# SQL Class
import asyncio


class SQLAdapter:
    _instance = None

    def __init__(self):
        """
        Initialises the SQL connection.
        """
        # Initialise the DB
        self.db = None
        pass

    # If the class is already initialised, return the instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQLAdapter, cls).__new__(cls)
        return cls._instance

    def close_db(self):
        """
        Closes the SQL database connection.
        """
        self.db.close()

    def get(self):
        """
        Fetches data from the SQL database. Dynamic arguments can be passed to fetch data
        from a specific collection, document or query.

        Args:


        Returns:
            None


        """
        return "Get data from SQL"

    def add(self, collection_path, data, document_id=None):
        """
        Adds a document to the SQL database.

        Args:


        Returns:
            None
        """
        return "Add data to SQL"

    def update(self):
        """
        Updates a document in the SQL database dynamically. Dynamic arguments can be passed to update data

        Args:


        Returns:
            None
        """
        return "Update data in SQL"

    def delete(self):
        """
        Deletes documents from the SQL database.

        Args:


        Returns:
            None
        """

        return "Delete data from SQL"

    # Add additional methods here