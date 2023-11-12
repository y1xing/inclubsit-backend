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
from .clubsSchema import *
from datetime import datetime

logging.basicConfig(level=logging.INFO)
# ??? not working - to be investigated
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

router = APIRouter(
    prefix="/clubs",
    tags=['clubs']
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

CLUB_UPDATE_PATH = "ClubUpdates"


######## GET REQUEST ############
@router.get("/{club_id}/profile")
async def get_club_profile(club_id: str, response: Response):
    """
    GET: Fetch a single club
    """

    return {"message": "club fetched successfully"}


@router.get("/{club_id}/members")
async def get_club_members(club_id: str, response: Response):
    """
    GET: Get members from a club
    """

    return {"message": "club fetched successfully"}


@router.get("/{club_id}/updates")
async def get_club_updates(club_id: str, response: Response):
    """
    GET: Get updates from a club
    """
    query = [("clubID", "==", int(club_id))]

    result = firebase_adapter.get(CLUB_UPDATE_PATH, query=query)

    return {"message": "club fetched successfully", "data": result}


######## POST REQUEST ############
@router.post("/{club_id}/updates")
async def post_club_updates(club_id: int, body: ClubUpdateSchema, response: Response):
    """
    POST: Add a new update for a club
    """
    
    data = dict(body)
    #set here as all new posts should by default have 0 likes
    data["clubID"] = club_id
    data["createdAt"] = datetime.now()
    #if post is an event add likes and likedBy 
    if data["postType"] == "event":
        data["likes"] = 0
        data["likedBy"] = []
    #if post is an update remove ctaLink
    elif data["postType"] == "update":
        data.pop("ctaLink")

    result = firebase_adapter.add(CLUB_UPDATE_PATH, data = data)


    return {"message": "update posted successfully"}#, 201


@router.post("/{club_id}/member", summary="Add Member")
async def add_club_member(body: dict, response: Response):
    """
    POST: Add member to club
    """

    return {"message": "Add member to club successfully"}


######## UPDATE/PUT REQUEST ############
@router.put("/{club_id}/profile")
async def update_club_profile(club_id: int, body: ClubProfileSchema, response: Response):
    """
    PUT: Update a club profile
    """

    #if field is empty, do not include it to be updated
    data = dict(body)
    #tuple to add all parameters to
    params = tuple()

    #dynamically create query from body
    query = """
        UPDATE Club SET ClubName = %s, ClubDescription = %s WHERE ClubID = %s;
    """

    # #if field is empty, get the current value from the database
    if data["ClubName"] == None or data["ClubName"] == "":
        #getting the current value from the database
        subquery = "SELECT ClubName FROM Club WHERE ClubID = %s;"
        result = sql_adapter.query(subquery, (club_id,))
        params += (str(result[0][0]),)
    else:
        params += (data["ClubName"],)

    if data["ClubDescription"] == None or data["ClubDescription"] == "":
        subquery = "SELECT ClubDescription FROM Club WHERE ClubID = %s;"
        result = sql_adapter.query(subquery, (club_id,))
        params += (str(result[0][0]),)
    else:
        params += (data["ClubDescription"],)

    #if field is empty, get the current value from the database
    # for key, value in data.items():
    #     if value == None or value == "":
    #         #getting the current value from the database
    #         subquery = "SELECT %s FROM Club WHERE ClubID = %s;"
    #         result = sql_adapter.query(subquery, (str(key).strip("'\""), club_id,))
    #         params += (str(result[0]),)
    #     else:
    #         params += (value,)

    params += (club_id,)

    try:
        sql_adapter.query(query, params)   
    except Exception as e:
        return {"error": str(e)}

    return {"message": "club profile updated successfully"}


@router.put("/{club_id}/updates")
async def update_club_updates(document_id: str, body: ClubUpdateSchema, response: Response):
    """
    GET: Add a new update for a club
    """

    data = dict(body)
    #if field is empty, do not include it to be updated
    for item in data:
        if data[item] == None or data[item] == "":
            data.pop(item)  

    firebase_adapter.update(CLUB_UPDATE_PATH, document_id=document_id, data=data)

    return {"message": "Update post updated successfully"}

#cdcca201-de7a-4e5c-b305-c01b53b85a6a
######## DELETE REQUEST ############
@router.delete("/{update_id}/updates")
async def delete_club_updates(update_id: str, response: Response):
    """
    DELETE: Delete a club
    """

    return {"message": "club deleted successfully"}


@router.delete("/{club_id}/member", summary="Remove Member")
async def delete_club_member(club_id: str, response: Response):
    """
    DELETE: Remove a member from club
    """

    return {"message": "Member removed successfully"}
