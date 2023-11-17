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

CATEGORY_IMAGE_PATH = "CategoryImages"
CLUBS_IMAGE_PATH = "ClubImages"

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
            "SELECT cc.ClubCategoryID, cc.ClubCategoryName, COUNT(*) FROM Club c LEFT JOIN ClubCategory cc on c.ClubCategoryID = cc.ClubCategoryID GROUP BY cc.ClubCategoryID")

        images = firebase_adapter.get_category_images()

        result_formatted = [
            {
                "id": category[0],
                "title": category[1],
                "media": images[str(category[0])]['image'],
                "numberOfClubs": category[1]
            } for category in result]

    except Exception as e:
        print("Error is", e)
        return {"message": "Error in fetching categories"}, 400

    return {"message": "All categories data fetched", "data": result_formatted}, 200


@router.get("/{category_id}")
async def get_category(category_id: str, response: Response):
    """
    GET: Get information on a category
    """

    try:
        print("Category_id", category_id)
        clubs = sql_adapter.query(
            "SELECT c.ClubID, c.ClubName, COUNT(*), c.ClubTrainingDates, c.ClubTrainingLocations FROM Club c LEFT JOIN ClubMember cm on c.ClubID = cm.ClubID WHERE c.ClubCategoryID = %s GROUP BY cm.ClubID", (category_id, ))
        category_info = sql_adapter.query(
            "SELECT c.ClubCategoryName, cc.CategoryDescription FROM ClubCategory c LEFT JOIN ClubCategoryInformation cc on c.ClubCategoryID = cc.ClubCategoryID WHERE cc.ClubCategoryID = %s", (category_id, ))[0]

        print('category_info', category_info)

        images = firebase_adapter.get_club_images()

        def members_estimate(members):
            if members <= 10:
                return "1-10"
            elif members > 10 and members <= 20:
                return "11-20"
            elif members > 20 and members <= 30:
                return "21-30"
            elif members > 30 and members <= 40:
                return "31-40"
            elif members > 40 and members <= 50:
                return "41-50"
            else:
                return "50+"

        result_formmated = {
            "category_info": {
                "title": category_info[0],
                "description": category_info[1],
            },
            "clubs": [
                {
                    "id": club[0],
                    "title": club[1],
                    "members": members_estimate(club[2]),
                    "training": club[3],
                    "location": club[4],
                    "media": images[str(club[0])]['logo']
                } for club in clubs]
        }

    except Exception as e:
        print(e)
        return {"message": "Error in fetching category"}, 400

    return {"message": "Category data fetched successfully", "data": result_formmated}, 200
