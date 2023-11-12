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
    403: {"description": "Not enough privileges"},
}

# Initialize Database
mongo_adapter = MongoAdapter()
sql_adapter = SQLAdapter()
firebase_adapter = Firebase()


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

    return {"message": "club fetched successfully"}


######## POST REQUEST ############
@router.post("/{club_id}/updates")
async def post_club_updates(club_id: str, body: dict, response: Response):
    """
    GET: Add a new update for a club
    """

    return {"message": "club fetched successfully"}


@router.post("/{club_id}/member", summary="Add Member")
async def add_club_member(body: dict, response: Response):
    """
    POST: Add member to club
    """

    return {"message": "Add member to club successfully"}


######## UPDATE/PUT REQUEST ############
@router.put("/{club_id}/profile")
async def update_club_profile(club_id: str, response: Response):
    """
    PUT: Update a club profile
    """

    return {"message": "club updated successfully"}


@router.put("/{club_id}/updates")
async def update_club_updates(club_id: str, body: dict, response: Response):
    """
    GET: Add a new update for a club
    """

    return {"message": "club fetched successfully"}


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
