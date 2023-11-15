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
async def get_club_profile(club_id: int, response: Response):
    """
    GET: Fetch a single club
    """
    columns = sql_adapter.query("SHOW COLUMNS FROM Club;")
    columns = [column[0] for column in columns]
    rows = sql_adapter.query(
        "SELECT c.ClubID, c.ClubName, cc.ClubCategoryName, c.ClubDescription, c.ClubTrainingDates, c.ClubTrainingLocations, c.ClubEmail, c.ClubInstagram FROM Club c LEFT JOIN ClubCategory cc ON c.ClubCategoryID = cc.ClubCategoryID WHERE c.ClubID = %s", (
            club_id, )
    )
    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

    result = dict(zip(columns, rows[0]))

    return {"message": "club fetched successfully", "data": result}


@router.get("/{club_id}/members")
async def get_club_members(club_id: int, response: Response):
    """
    GET: Get members from a club
    """

    rows = sql_adapter.query(
        "SELECT a.FirstName, a.LastName, at.TypeName, a.MatriculationYear, ci.CourseName FROM Account a RIGHT JOIN ClubMember cm ON a.StudentID = cm.StudentID LEFT JOIN AccountType at ON cm.AccountTypeID = at.AccountTypeID LEFT JOIN CourseInformation ci ON a.CourseID = ci.CourseID WHERE cm.ClubID = %s",
        (club_id,)
    )
    if len(rows) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

    result = [{
        "first_name": first_name, "last_name": last_name, "role": role,
        "matriculation_year": matriculation_year, "course_name": course_name
    } for first_name, last_name, role, matriculation_year, course_name in rows]

    return {"message": "club fetched successfully", "data": result}


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
async def post_club_updates(club_id: str, body: dict, response: Response):
    """
    GET: Add a new update for a club
    """

    return {"message": "club fetched successfully"}


# @router.post("/{club_id}/member", summary="Add Member")
# async def add_club_member(body: dict, response: Response):
#     """
#     POST: Add member to club
#     """


#     return {"message": "Add member to club successfully"}

@router.post("/{club_id}/member", summary="Add Member")
async def add_club_member(club_id: int, body: dict, response: Response):
    """
    POST: Add member to club
    """
    student_id = body.get("StudentID")
    account_type_id = 1

    if not student_id:
        raise HTTPException(status_code=400, detail="Missing studentID.")

    insert_query = "INSERT INTO ClubMember (ClubID, StudentID, AccountTypeID) VALUES (%s, %s, %s);"
    values = (club_id, student_id,1)

    try:
        sql_adapter.query(insert_query, values)
    except Exception as e:
        response.status_code = 500
        return {"message": "An error occurred.", "error": str(e)}

    return {"message": "Member added to club successfully"}


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
    DELETE: Delete a club update
    """
    query = firebase_adapter.delete(CLUB_UPDATE_PATH, update_id)

    return {"message": "club update deleted successfully"}
    

@router.delete("/clubs/{club_id}/member", summary="Remove Member")
async def delete_club_member(club_id: int,body: dict, response: Response):
    """
    DELETE: Remove a member from a club
    """
    student_id = body.get("StudentID")

    if not student_id:
        raise HTTPException(status_code=400, detail="Missing studentID.")

    delete_query = "DELETE FROM ClubMember WHERE ClubID = %s AND StudentID = %s;"
    values = (club_id, student_id)

    try:
        sql_adapter.query(delete_query, values)
    except Exception as e:
        response.status_code = 500
        return {"message": "An error occurred.", "error": str(e)}

    return {"message": "Member removed from club successfully"}