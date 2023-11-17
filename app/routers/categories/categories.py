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
    GET: Get all categories information including the member count
    """
    try:
        result = sql_adapter.query(
            "SELECT cc.ClubCategoryName, COUNT(*) FROM Club c LEFT JOIN ClubCategory cc on c.ClubCategoryID = cc.ClubCategoryID GROUP BY cc.ClubCategoryID")

        result_formatted = [{"name": category[0],
                             "clubs": category[1]} for category in result]

    except Exception as e:
        print(e)
        return {"message": "Error in fetching categories"}, 400

    return {"message": "All categories data fetched", "data": result_formatted}, 200


@router.get("/{category_id}")
async def get_category(category_id: str, response: Response):
    """
    GET: Get information on a category
    """

    try:
        clubs = sql_adapter.query(
            "SELECT c.ClubID, c.ClubName, COUNT(*), c.ClubTrainingDates, c.ClubTrainingLocations FROM Club c LEFT JOIN ClubMember cm on c.ClubID = cm.ClubID WHERE c.ClubCategoryID = %s GROUP BY cm.ClubID", (category_id, ))
        category_info = sql_adapter.query(
            "SELECT c.ClubCategoryName, cc.CategoryDescription FROM ClubCategoryInformation cc, ClubCategory c WHERE c.ClubCategoryID = %s", (category_id, ))[0]

        result_formmated = {
            "category_info": {
                "name": category_info[0],
                "description": category_info[1],
            },
            "clubs": [
                {
                    "id": club[0],
                    "title": club[1],
                    "members": club[2],
                    "training": club[3],
                    "location": club[4],
                } for club in clubs]
        }

    except Exception as e:
        print(e)
        return {"message": "Error in fetching category"}, 400

    return {"message": "Category data fetched successfully", "data": result_formmated}
