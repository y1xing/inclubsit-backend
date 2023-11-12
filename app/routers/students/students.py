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
    403: {"description": "Not enough privileges"},
}

# Initialize Database
mongo_adapter = MongoAdapter()
sql_adapter = SQLAdapter()
firebase_adapter = Firebase()

#### Standard API endpoints ####


@router.get("/all")
async def all(response: Response):
    """
    GET: Fetch all the students data for the overview screen and redux
    """

    result = crud.get('student')

    return {"message": "All students data fetched successfully", "data": result}

# CRUD operations for single student


@router.get("/{student_id}")
async def get_student(student_id: str, response: Response):
    """
    GET: Fetch a single student
    """

    return {"message": "student fetched successfully"}


@router.post("/")
async def add_student(body: dict, response: Response):
    """
    POST: Add a new student
    """

    return {"message": "student added successfully"}


@router.put("/{student_id}")
async def update_student(student_id: str, response: Response):
    """
    PUT: Update a student
    """

    return {"message": "student updated successfully"}


@router.delete("/{student_id}")
async def delete_student(student_id: str, response: Response):
    """
    DELETE: Delete a student
    """

    return {"message": "student deleted successfully"}
