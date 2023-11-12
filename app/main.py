from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
import os
import uvicorn

# Import the different routers like /user /clubs
from routers.example import example
from routers.clubs import clubs
from routers.students import students
from routers.categories import categories

# Import the different database adapters
from config.firebase import Firebase
from config.mongo import MongoAdapter
from config.sql import SQLAdapter
from dotenv import load_dotenv

load_dotenv()


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
app = FastAPI(title="InClubSIT Backend", version="0.5")

# Include the different routers
app.include_router(example.router)
app.include_router(students.router)
app.include_router(clubs.router)
app.include_router(categories.router)

# Violating PEP 8 to overcome circular imports

mongo_adapter = None
sql_adapter = None

# Initialise connect with MongoDB and SQL


async def initialise_database():
    # Initialiase the DB
    global mongo_adapter
    global sql_adapter

    print("Initialising DB")
    mongo_adapter = MongoAdapter()
    sql_adapter = SQLAdapter()
    firebase_adapter = Firebase()

# Close the database


async def close_database():
    # Close the db
    print("Closing DB")
    mongo_adapter.close_db()
    sql_adapter.close_db()
    pass


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For when the app starts and shuts down
app.add_event_handler("startup", initialise_database)
app.add_event_handler("shutdown", close_database)


@app.get("/")
async def root():

    return {"api_status": "online", "username": "none", "data": "API is working"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost",
                port=8001, reload=True, reload_dirs=".")
