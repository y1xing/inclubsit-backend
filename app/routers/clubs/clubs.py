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
crud = Firebase()
mongo_adapter = MongoAdapter()
sql_adapter = SQLAdapter()


#### Standard API endpoints ####
@router.get("/all")
async def all(response: Response):
    """
    GET: Fetch all the clubs data for the overview screen and redux
    """

    result = crud.get('club')

    return {"message": "All clubs data fetched successfully", "data": result}

# CRUD operations for single club


@router.get("/{club_id}")
async def get_club(club_id: str, response: Response):
    """
    GET: Fetch a single club
    """

    return {"message": "club fetched successfully"}


# Change the body: dict to body: schemaModal
@router.post("/createClub")
async def add_club(body: dict, response: Response):
    """
    POST: Add a new club
    """

    return {"message": "club added successfully"}


@router.put("/{club_id}")
async def update_club(club_id: str, response: Response):
    """
    PUT: Update a club
    """

    return {"message": "club updated successfully"}


@router.delete("/{club_id}")
async def delete_club(club_id: str, response: Response):
    """
    DELETE: Delete a club
    """

    return {"message": "club deleted successfully"}

#Club Member
@router.post("/addMember", summary="Add Member")
async def add_club(body: dict, response: Response):
    """
    POST: Add member to club
    """

    return {"message": "Add member to club successfully"}

@router.delete("/removeMember", summary="Remove Member")
async def delete_club(club_id: str, response: Response):
    """
    DELETE: Remove a member from club
    """

    return {"message": "Member removed successfully"}

#Student Leader
@router.post("/addStudentLeader", summary="Add Student Leader")
async def add_club(body: dict, response: Response):
    """
    POST: Add Student Leader to club
    """

    return {"message": "Add member to club successfully"}

@router.delete("/removeStudentLeader", summary="Remove Student Leader")
async def delete_club(club_id: str, response: Response):
    """
    DELETE: Remove Student Leader from club
    """

    return {"message": "Student Leader removed successfully"}