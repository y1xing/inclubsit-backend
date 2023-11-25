import os
import logging
import random as rand
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
    try:
        print(student_id)
        # Get the clubs that a user is member of with SQL based on user_id
        clubs = sql_adapter.query(
            "SELECT ClubID FROM ClubMember WHERE StudentID = %s",  (student_id,))
        # Get the updates based on the clubs retrieved
        updates_list = []
        for club in clubs:
            club_updates = firebase_adapter.get(
                collection_path="ClubUpdates",  # Firestore collection name
                # Query based on 'clubid' field in Firestore documents
                query=[("clubID", "==", club[0])]
            )

            name = sql_adapter.query(
                "SELECT ClubName FROM Club WHERE ClubID = %s", (club[0],))
            images = firebase_adapter.get_club_images()
            image = images[str(club[0])]['logo']
            for i in range(len(club_updates)):
                club_updates[i]["clubName"] = name[0][0]
                club_updates[i]["logo"] = image
            if club_updates:
                updates_list.extend(club_updates)

        # Optional: Sort the updates by a relevant field such as 'date'
        updates_list.sort(key=lambda x: x.get('createdAt', ''), reverse=True)

        return {"message": "All student's updates fetched successfully", "data": updates_list}

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(e)}


@router.get("/{student_id}/recommended")
async def get_student_recommended(student_id: str, response: Response):
    """
    GET: Get the recommended clubs for a student
    """

    counts = sql_adapter.query("SELECT C.ClubCategoryID \
                                FROM ClubMember AS CM, Club AS C \
                                WHERE CM.StudentID = %s \
                                AND CM.ClubID = C.ClubID \
                                GROUP BY C.ClubCategoryID \
                                ORDER BY COUNT(C.ClubCategoryID)\
                                DESC LIMIT 1", (student_id,))
    print(counts)
    # If the student is not part of any club, recommend random clubs
    # 7 = SMC, therefore suggest a random club from other categories
    if counts[0][0] == 1:
        category = rand.randint(1, 6)
    else:
        category = counts[0][0]

    clubs = sql_adapter.query("SELECT C.ClubID, C.ClubName, CC.ClubCategoryName \
        FROM Club AS C \
        JOIN ClubCategory AS CC ON C.ClubCategoryID = CC.ClubCategoryID \
        WHERE C.ClubCategoryID = %s \
        AND C.ClubCategoryID = CC.ClubCategoryID \
        AND C.ClubID NOT IN (SELECT ClubID FROM ClubMember WHERE StudentID = %s) \
        ORDER BY RAND() LIMIT 5", (category, student_id,))    
    images = firebase_adapter.get_club_images()
    result = [club + (images[str(club[0])]['logo'],) for club in clubs]

    return {"message": "All students data fetched successfully", "data": result}


@router.get("/{student_id}/clubs")
async def get_student_clubs(student_id: str, response: Response):
    """
    GET: Get all the clubs the student is part of
    """
    # Get the clubs that a user is member of with SQL based on user_id
    clubs = sql_adapter.query(
        "SELECT c.ClubID, c.ClubName, c.ClubDescription  FROM Club c INNER JOIN ClubMember cm ON c.ClubID = cm.ClubID WHERE cm.StudentID = %s",  (student_id,))

    images = firebase_adapter.get_club_images()
    result = [club + (images[str(club[0])]['logo'],) for club in clubs]
    return {"message": "All student's club data fetched successfully", "data": result}


@router.get("/{student_id}/profile")
async def get_student_data(student_id: int, response: Response):
    """
    GET: Get a student's data
    """
    query = """
    SELECT a.StudentID, a.Email, a.FirstName, a.LastName, a.MatriculationYear, a.CourseID, a.Gender, ci.CourseName
    FROM Account a
    JOIN CourseInformation ci ON a.CourseID = ci.CourseID
    WHERE a.StudentID = %s;
    """
    columns = sql_adapter.query("SHOW COLUMNS FROM Account;")
    columns += sql_adapter.query(
        "SHOW COLUMNS FROM CourseInformation WHERE Field='CourseName';")

    print(columns)
    row = sql_adapter.query(query, (student_id,))

    if len(row) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")

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
        return {"message": "Student is not a member", "data": 0}, 200

    return {"message": "Student's role fetched successfully", "data": row[0][0]}, 200
