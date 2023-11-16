# Firebase Class
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import asyncio


import firebase_admin
from firebase_admin import credentials, firestore, storage


class Firebase:
    _instance = None

    def __init__(self):
        """
        Initializes the Firebase instance.

        This constructor checks if the Firebase app has already been initialized and
        either initializes a new app or uses an existing one.

        Raises:
            Exception: If unable to initialize Firebase.
        """
        try:
            self.cred = credentials.Certificate('config/key.json')
        except Exception as e:
            self.cred = credentials.Certificate('../../config/key.json')

        # Check if the app has already been initialized
        if not firebase_admin._apps:
            self.app = firebase_admin.initialize_app(self.cred, {
                'storageBucket': 'bts-cms.appspot.com',
            })
        else:
            # If the app is already initialized, use the existing app
            self.app = firebase_admin._apps

        self.db = firestore.client()
        self.bucket = storage.bucket()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Firebase, cls).__new__(cls)
        return cls._instance

    def close_db(self):
        """
        Closes the Firestore database connection.
        """
        self.db.close()

    def get(self, collection_path, document_id=None, query=None, queryType="and"):
        """
        Fetches data from the Firestore database.

        Args:
            collection_path (str): The path to the Firestore collection.
            document_id (str, optional): The ID of the specific document to fetch.
            query (list, optional): A list of query filters to apply when fetching documents.
            queryType (str): The type of query to perform ('and' or 'or') when multiple filters are provided.

        Returns:
            dict or list: The fetched data as a dictionary (for single document) or a list of dictionaries (for multiple documents).

        Raises:
            Exception: If an error occurs during database access.
        """
        try:
            collection_ref = self.db.collection(collection_path)

            if document_id:
                # Case 2: Fetch a specific document
                doc_ref = collection_ref.document(document_id)
                doc = doc_ref.get()
                if doc.exists:
                    return doc.to_dict()
                else:
                    raise Exception("Document not found")

            elif query:
                # Case 3: Fetch documents based on a query
                # If there is a query, we need to loop through each of the queries
                filters = []
                for filter in query:
                    field, operator, value = filter
                    filters.append(firestore.FieldFilter(
                        field, operator, value))

                if queryType == "or":
                    final_query = firestore.Or(filters=filters)
                else:
                    final_query = firestore.And(filters=filters)

                collection_ref = collection_ref.where(filter=final_query)
                documents = collection_ref.stream()
                result = [doc.to_dict() for doc in documents]
                return result

            else:
                # Case 1: Fetch all data from the collection
                documents = collection_ref.stream()
                result = [doc.to_dict() for doc in documents]
                return result

        except Exception as e:
            # Handle exceptions and return appropriate error messages
            return str(e)

    def add(self, collection_path, data, document_id=None):
        """
        Adds a document to the Firestore database.

        Args:
            collection_path (str): The path to the Firestore collection.
            data (dict): The data to be added as a dictionary.
            document_id (str, optional): The ID of the specific document to add.

        Returns:
            None
        """
        collection_ref = self.db.collection(collection_path)
        if document_id:
            # Case 1: Add a document with a specific ID
            doc_ref = collection_ref.document(document_id)
            doc_ref.set(data)
        else:
            # Case 2: Add a document with a random ID
            collection_ref.add(data)

    def update(self, collection_path, document_id, data):
        """
        Updates a document in the Firestore database.

        Args:
            collection_path (str): The path to the Firestore collection.
            document_id (str): The ID of the specific document to update.
            data (dict): The data to be updated as a dictionary.

        Returns:
            None
        """
        collection_ref = self.db.collection(collection_path)
        doc_ref = collection_ref.document(document_id)
        doc_ref.update(data)

    def delete(self, collection_path, document_id=None, query=None, queryType="and"):
        """
        Deletes documents from the Firestore database.

        Args:
            collection_path (str): The path to the Firestore collection.
            document_id (str, optional): The ID of the specific document to delete.
            query (list, optional): A list of query filters to apply when deleting documents.

        Returns:
            None
        """
        collection_ref = self.db.collection(collection_path)
        if document_id:
            # Case 1: Delete a specific document
            doc_ref = collection_ref.document(document_id)
            doc_ref.delete()
        elif query:
            # Case 2: Delete all documents that match the query
            # If there is a query, we need to loop through each of the queries
            filters = []
            for filter in query:
                field, operator, value = filter
                filters.append(firestore.FieldFilter(field, operator, value))

            if queryType == "or":
                final_query = firestore.Or(filters=filters)
            else:
                final_query = firestore.And(filters=filters)

            collection_ref = collection_ref.where(filter=final_query)
            documents = collection_ref.stream()
            for doc in documents:
                doc.reference.delete()
        else:
            # Case 3: Delete all documents in the collection
            documents = collection_ref.stream()
            for doc in documents:
                doc.reference.delete()

    def increment(self, collection_path, document_id=None, query=None, field=None, value=1):
        """
        Increments fields in documents in the Firestore database.

        Args:
            collection_path (str): The path to the Firestore collection.
            document_id (str, optional): The ID of the specific document to update.
            query (list, optional): A list of query filters to apply when updating documents.
            field (str): The field to increment.
            value (int): The value by which to increment the field.

        Returns:
            None
        """
        collection_ref = self.db.collection(collection_path)
        if query:
            # Case 1: Increment all documents that match the query
            # If there is a query, we need to loop through each of the queries
            filters = []
            for filter in query:
                field, operator, value = filter
                filters.append(firestore.FieldFilter(field, operator, value))

            final_query = firestore.And(filters=filters)
            collection_ref = collection_ref.where(filter=final_query)
            documents = collection_ref.stream()
            for doc in documents:
                doc.reference.update({field: firestore.Increment(value)})
        else:
            # Case 2: Increment a specific document
            doc_ref = collection_ref.document(document_id)
            doc_ref.update({field: firestore.Increment(value)})

    def remove_from_array(self, collection_path, document_id, array_field, item):
        """
        Removes an item from an array field in a Firestore document.

        Args:
            collection_path (str): The path to the Firestore collection.
            document_id (str): The ID of the specific document to update.
            array_field (str): The name of the array field in the document.
            item: The item to be removed from the array field.
        """
        try:
            collection_ref = self.db.collection(collection_path)
            doc_ref = collection_ref.document(document_id)

            # Firestore operation to remove the item from the array
            doc_ref.update({array_field: firestore.ArrayRemove([item])})
            return True
        except Exception as e:
            print(f"Error removing item from array: {e}")
            return False

    def add_to_array(self, collection_path, document_id, array_field, item):
        """
        Adds an item to an array field in a Firestore document.

        Args:
            collection_path (str): The path to the Firestore collection.
            document_id (str): The ID of the specific document to update.
            array_field (str): The name of the array field in the document.
            item: The item to be added to the array field.
        """
        try:
            collection_ref = self.db.collection(collection_path)
            doc_ref = collection_ref.document(document_id)

            # Firestore operation to add the item to the array
            doc_ref.update({array_field: firestore.ArrayUnion([item])})
            return True
        except Exception as e:
            print(f"Error adding item to array: {e}")
            return False