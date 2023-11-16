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
        #Get the clubs that a user is member of with SQL based on user_id
        clubs = sql_adapter.query("SELECT ClubID FROM ClubMember WHERE StudentID = %s",  (student_id,))
        #Get the updates based on the clubs retrieved
        updates_list = []
        for club in clubs:
            club_updates = firebase_adapter.get(
                collection_path="ClubUpdates",  # Firestore collection name
                query=[("clubID", "==", club[0])]  # Query based on 'clubid' field in Firestore documents
            )
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
    GET: Get the recommendec clubs for a student
    """

    counts = sql_adapter.query("SELECT C.ClubCategoryID \
                                FROM ClubMember AS CM, Club AS C \
                                WHERE CM.StudentID = %s \
                                AND CM.ClubID = C.ClubID \
                                GROUP BY C.ClubCategoryID \
                                ORDER BY COUNT(C.ClubCategoryID)\
                                DESC LIMIT 1",(student_id,))
    print(counts)
    # If the student is not part of any club, recommend random clubs
    # 1 = SMC, therefore suggest a random club from other categories
    if counts[0][0] == 1:
        category = rand.randint(2, 7)
    else:
        category = counts[0][0]
        
    result = sql_adapter.query("SELECT ClubName, ClubID FROM club WHERE ClubCategoryID = %s ORDER BY RAND() LIMIT 5",(category,))

    return {"message": "All students data fetched successfully", "data": result}


@router.get("/{student_id}/clubs")
async def get_student_clubs(student_id: str, response: Response):
    """
    GET: Get all the clubs the student is part of
    """
    #Get the clubs that a user is member of with SQL based on user_id
    clubs = sql_adapter.query("SELECT c.ClubName, c.ClubID FROM Club c INNER JOIN ClubMember cm ON c.ClubID = cm.ClubID WHERE cm.StudentID = %s",  (student_id,))
    
    return {"message": "All student's club data fetched successfully", "data": clubs}

@router.get("/student/{student_id}/profile")
async def get_student_data(student_id: int, response: Response):
    """
    GET: Get a student's data
    """
    query = """
    SELECT a.StudentID, a.Email, a.FirstName, a.LastName, a.MatriculationYear, ci.CourseID, ci.CourseName
    FROM Account a
    JOIN CourseInformation ci ON a.CourseID = ci.CourseID
    WHERE a.StudentID = %s;
    """
    values = (student_id,)
    try:
        row = sql_adapter.query(query, values)
        if row:
            student_data = row[0]
            result = {
                "StudentID": student_data[0],
                "Email": student_data[1],
                "FirstName": student_data[2],
                "LastName": student_data[3],
                "MatriculationYear": student_data[4],
                "CourseID": student_data[5],
                "CourseName": student_data[6],
            }
            return {"message": "Student's data fetched successfully.", "data": result}
        else:
            raise HTTPException(status_code=404, detail="Student not found.")
    except Exception as e:
        response.status_code = 500
        return {"message": "An error occurred.", "error": str(e)}


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