crud = None

COLLECTION_PATH = "TEST_COLLECTION"

### GET FUNCTIONS ###
# Get all data from a collection, returns an list of dictionaries
result = crud.get(COLLECTION_PATH)

# Get a single document from a collection, returns a dictionary
result = crud.get(COLLECTION_PATH, document_id="DOCUMENT_ID")

# Get documents from a collection based on a query, returns a list of dictionaries
# Query format: [(field, operator, value), (field, operator, value)]
query = [("id", "==", "ad-123445"), ("district", "==", "Punggol")]
queryType = "and" # or

result = crud.get(COLLECTION_PATH, query=query, queryType=queryType)


### ADD FUNCTIONS ###
# Add a document to a collection with a specific ID
data = {"id": "ad-123445", "district": "Punggol"}
crud.add(COLLECTION_PATH, data=data, document_id="DOCUMENT_ID")

# Add a document to a collection with a random ID
crud.add(COLLECTION_PATH, data=data)


### UPDATE FUNCTIONS ###
# Original Data in Firestore: {"id": "ad-123445", "district": "Punggol"}
# You want to update the district to "Sengkang"
data = {"district": "Sengkang"}
crud.update(COLLECTION_PATH, document_id="DOCUMENT_ID", data=data)

### DELETE FUNCTIONS ###
# 3 Scenarios:
# 1. Delete a specific document
# 2. Delete all documents that match a query
# 3. Delete all documents in a collection

# Case 1: Delete a specific document
crud.delete(COLLECTION_PATH, document_id="DOCUMENT_ID")

# Case 2: Delete all documents that match the query
query = [("id", "==", "ad-123445")]
crud.delete(COLLECTION_PATH, query=query)

# Case 3: Delete all documents in a collection
crud.delete(COLLECTION_PATH)




