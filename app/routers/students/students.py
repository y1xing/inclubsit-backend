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
async def get_student_updates(student_id: str, response: Response):
    """
    GET: Get the profile of the student
    """

    result = None

    return {"message": "All students data fetched successfully", "data": result}


@router.get("/{student_id}/{club_id}/role")
async def get_student_updates(student_id: str, club_id: str, response: Response):
    """
    GET: Get the role of the student in a club
    """

    result = None

    return {"message": "All students data fetched successfully", "data": result}
