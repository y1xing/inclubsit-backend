# MongoDB Class
import asyncio


class MongoAdapter:
    _instance = None

    def __init__(self):
        """
        Initialises the MongoDB connection.
        """
        # Initialise the DB
        self.db = None
        pass

    # If the class is already initialised, return the instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoAdapter, cls).__new__(cls)
        return cls._instance

    def close_db(self):
        """
        Closes the mongoDB database connection.
        """
        self.db.close()

    def get(self):
        """
        Fetches data from the mongoDB database. Dynamic arguments can be passed to fetch data
        from a specific collection, document or query.

        Args:


        Returns:
            None


        """
        return "Get data from MongoDB"

    def add(self, collection_path, data, document_id=None):
        """
        Adds a document to the mongoDB database.

        Args:


        Returns:
            None
        """
        return "Add data to MongoDB"

    def update(self):
        """
        Updates a document in the mongoDB database dynamically. Dynamic arguments can be passed to update data

        Args:


        Returns:
            None
        """
        return "Update data in MongoDB"

    def delete(self):
        """
        Deletes documents from the mongoDB database.

        Args:


        Returns:
            None
        """

        return "Delete data from MongoDB"

    # Add additional methods here