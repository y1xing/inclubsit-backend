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
from .studentsSchema import *


logging.basicConfig(level=logging.INFO)
# ??? not working - to be investigated
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

router = APIRouter(
    prefix="/students",
    tags=['students']
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

############ GET REQUESTS ############


@router.get("/{student_id}/updates")
async def get_student_updates(student_id: str, response: Response):
    """
    GET: Get all the updates from the clubs that student is part of
    """

    result = None

    return {"message": "All students data fetched successfully", "data": result}


@router.get("/{student_id}/recommended")
async def get_student_recommended(student_id: str, response: Response):
    """
    GET: Get the recommendec clubs for a student
    """

    result = None

    return {"message": "All students data fetched successfully", "data": result}


@router.get("/{student_id}/clubs")
async def get_student_clubs(student_id: str, response: Response):
    """
    GET: Get all the clubs the student is part of
    """

    result = None

    return {"message": "All students data fetched successfully", "data": result}


@router.get("/{student_id}/profile")
async def get_student_profile(student_id: int, response: Response):
    """
    GET: Get the profile of the student
    """

    columns = sql_adapter.query("SHOW COLUMNS FROM Account;")
    row = sql_adapter.query(
        "SELECT * FROM Account WHERE StudentID = %s", (student_id,))
    if len(row) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail="Student not found.")
    result = dict(zip((column[0] for column in columns), row[0]))

    return {"message": "Student's data fetched successfully.", "data": result}


@router.get("/{student_id}/{club_id}/role")
async def get_student_role(student_id: int, club_id: int, response: Response):
    """
    GET: Get the role of the student in a club
    """

    row = sql_adapter.query(
        "SELECT at.AccountTypeID, at.TypeName FROM ClubMember cm LEFT JOIN AccountType at ON cm.AccountTypeID = at.AccountTypeID WHERE cm.StudentID = %s AND cm.ClubID = %s", (
            student_id, club_id,)
    )

    if len(row) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=404, detail="Student not found or not part of the club.")

    result = {
        "account_type_id": row[0][0],
        "account_type_name": row[0][1]
    }

    return {"message": "Student's role fetched successfully", "data": result}
