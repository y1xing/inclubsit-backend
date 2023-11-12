import os
import logging

# from config import conf
from fastapi import APIRouter, Cookie, Form, status, Body, Depends, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from config.firebase import Firebase
from config.mongo import MongoAdapter
from config.sql import SQLAdapter
from config.constants import *

# Import the schemas
from .categoriesSchema import *


logging.basicConfig(level=logging.INFO)
# ??? not working - to be investigated
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

router = APIRouter(
    prefix="/categories",
    tags=['categories']
)


auth_responses = {
    200: {"description": "OK"},
    201: {"description": "Created"},
    204: {"description": "No Content"},
    400: {"description": "Bad Request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    404: {"description": "Not Found"},
    500: {"description": "Internal Server Error"},
}

# Initialize Database
mongo_adapter = MongoAdapter()
sql_adapter = SQLAdapter()
firebase_adapter = Firebase()


#### Standard API endpoints ####
@router.get("/all")
async def all(response: Response):
    """
    GET: Get all categories information
    """
    try:
        result = sql_adapter.query("SELECT * FROM ClubCategory")
    except Exception as e:
        print(e)
        return {"message": "Error in fetching categories"}, 400

    return {"message": "All categories data fetched", "data": result}, 200


@router.get("/{category_id}")
async def get_category(category_id: str, response: Response):
    """
    GET: Get information on a category
    """

    result = None

    return {"message": "Category data fetched successfully", "data": result}
