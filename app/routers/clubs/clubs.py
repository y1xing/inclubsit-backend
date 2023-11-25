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
async def get_club_profile(club_id: int, response: Response):
    """
    GET: Fetch a single club
    """
    images = firebase_adapter.get_club_images()

    columns = sql_adapter.query("SHOW COLUMNS FROM Club;")
    columns = [column[0] for column in columns]
    rows = sql_adapter.query(
        "SELECT c.ClubID, c.ClubName, cc.ClubCategoryName, c.ClubDescription, c.ClubTrainingDates, c.ClubTrainingLocations, c.ClubEmail, c.ClubInstagram FROM Club c LEFT JOIN ClubCategory cc ON c.ClubCategoryID = cc.ClubCategoryID WHERE c.ClubID = %s", (
            club_id, )
    )

    columns.append("logo")
    columns.append("cover")

    rows = [row + (images[str(row[0])]['logo'], images[str(row[0])]['cover'])
            for row in rows]

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

    # Get leaders data also
    leaders = sql_adapter.query(
        """
        SELECT at.TypeName, a.FirstName, a.LastName, a.MatriculationYear, co.CourseName
        FROM ClubMember c
        LEFT JOIN Account a ON a.StudentID = c.StudentID
        LEFT JOIN CourseInformation co ON a.CourseID = co.CourseID
        INNER JOIN AccountType at ON at.AccountTypeID = c.AccountTypeID
        WHERE c.ClubID = %s AND c.AccountTypeID > 1
        """,
        (club_id,)
    )

    # Add to leader list
    leaders = [
        {
            "role": leader[0],
            "name": f"{leader[1]} {leader[2]}",
            "course": leader[4],
            "year": int(datetime.now().year) - int(leader[3]) + 1,

        } for leader in leaders
    ]

    result = dict(zip(columns, rows[0]))

    return {"message": "club fetched successfully", "data": {
        "profile": result,
        "leaders": leaders
    }}, 200


@ router.get("/{club_id}/members")
async def get_club_members(club_id: int, response: Response):
    """
    GET: Get members from a club
    """

    rows = sql_adapter.query(
        """
        SELECT a.StudentID, a.FirstName, a.LastName, at.TypeName, a.MatriculationYear, a.Gender, ci.CourseName, cl.ClusterName
        FROM Account a 
        RIGHT JOIN ClubMember cm ON a.StudentID = cm.StudentID 
        LEFT JOIN AccountType at ON cm.AccountTypeID = at.AccountTypeID 
        LEFT JOIN CourseInformation ci ON a.CourseID = ci.CourseID 
        INNER JOIN Cluster cl ON cl.ClusterID = ci.ClusterID
        WHERE cm.ClubID = %s
        """,
        (club_id,)
    )
    if len(rows) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

    result = [{
        "studentId": student_id,
        "name": f"{first_name} {last_name}",
        "role": role,
        "year": int(datetime.now().year) - int(matriculation_year) + 1,
        "gender": gender,
        "course": course_name,
        "cluster": cluster,
    } for student_id, first_name, last_name, role, matriculation_year, gender, course_name, cluster in rows]

    return {"message": "club fetched successfully", "data": result}, 200


@ router.get("/{club_id}/updates")
async def get_club_updates(club_id: str, response: Response):
    """
    GET: Get updates from a club
    """
    query = [("clubID", "==", int(club_id))]

    result = firebase_adapter.get(CLUB_UPDATE_PATH, query=query)

    # Sort result by createdAt, earliest to oldest
    sorted_posts = sorted(result, key=lambda x: x['createdAt'], reverse=True)

    return {"message": "club fetched successfully", "data": sorted_posts}, 200


######## POST REQUEST ############
@ router.post("/{club_id}/updates")
async def post_club_updates(club_id: int, body: ClubUpdateSchema, response: Response):
    """
    POST: Add a new update for a club
    """

    data = dict(body)
    # set here as all new posts should by default have 0 likes
    data["clubID"] = club_id
    data["createdAt"] = datetime.utcnow()
    # if post is an event add likes and likedBy
    if data["postType"] == "event":
        data["likes"] = 0
        data["likedBy"] = []
    # if post is an update remove ctaLink
    elif data["postType"] == "update":
        data.pop("ctaLink")

    elif data['media'] == None:
        data.pop("media")

    print(data)

    result = firebase_adapter.add(
        CLUB_UPDATE_PATH, data=data, document_id=data['id'])

    data['createdAt'] = datetime.now()

    return {"message": "update posted successfully", "data": data}  # , 201


# @router.post("/{club_id}/member", summary="Add Member")
# async def add_club_member(body: dict, response: Response):
#     """
#     POST: Add member to club
#     """


#     return {"message": "Add member to club successfully"}

@ router.post("/{club_id}/member", summary="Add Member")
async def add_club_member(club_id: int, body: dict, response: Response):
    """
    POST: Add member to club
    """
    student_id = body.get("StudentID")
    account_type_id = 1

    if not student_id:
        raise HTTPException(status_code=400, detail="Missing studentID.")

    insert_query = "INSERT INTO ClubMember (ClubID, StudentID, AccountTypeID) VALUES (%s, %s, %s);"
    values = (club_id, student_id, 1)

    try:
        sql_adapter.query(insert_query, values)
    except Exception as e:
        response.status_code = 500
        return {"message": "An error occurred.", "error": str(e)}

    return {"message": "Member added to club successfully"}


######## UPDATE/PUT REQUEST ############
@ router.put("/{club_id}/profile")
async def update_club_profile(club_id: int, body: ClubProfileSchema, response: Response):
    """
    PUT: Update a club profile
    """

    # if field is empty, do not include it to be updated
    data = dict(body)
    # tuple to add all parameters to
    params = tuple()

    # dynamically create query from body
    query = """
        UPDATE Club SET ClubDescription = %s, ClubTrainingDates = %s, ClubTrainingLocations = %s, ClubEmail = %s, ClubInstagram = %s WHERE ClubID = %s;
    """

    email = data['email']
    description = data['description']
    instagram = data['instagram']
    location = data['location']
    training = data['training']

    params = (description, training, location, email, instagram, club_id)

    try:
        sql_adapter.query(query, params)
    except Exception as e:
        return {"error": str(e)}

    return {"message": "club profile updated successfully"}


@ router.put("/{post_id}/updates")
async def update_club_updates(post_id: str, body: dict, response: Response):
    """
    GET: Add a new update for a club
    """

    data = dict(body)
    # if field is empty, do not include it to be updated
    for item in data:
        if data[item] == None or data[item] == "":
            data.pop(item)

    firebase_adapter.update(
        CLUB_UPDATE_PATH, document_id=post_id, data=data)

    return {"message": "Update post updated successfully", "data": data}

# cdcca201-de7a-4e5c-b305-c01b53b85a6a
######## DELETE REQUEST ############


@router.delete("/{update_id}/updates")
async def delete_club_updates(update_id: str, response: Response):
    """
    DELETE: Delete a club update
    """
    query = firebase_adapter.delete(CLUB_UPDATE_PATH, update_id)

    return {"message": "club update deleted successfully"}


@router.delete("/{club_id}/member/{student_id}", summary="Remove Member")
async def delete_club_member(club_id: int, student_id: str, response: Response):
    """
    DELETE: Remove a member from a club
    """

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

######## LIKE POST ############


@router.put("/{update_id}/increaseLike")
async def increase_update_likes(update_id: str, user_id: str, response: Response):
    """
    PUT: increase Like
    """

    collection_id = "ClubUpdates"
    result = firebase_adapter.increment(
        collection_id, document_id=update_id, field="likes")
    print(result)

    data = "likedBy:"
    result2 = firebase_adapter.add_to_array(
        collection_id, update_id, "likedBy", user_id)
    print(result2)

    return {
        "status": 200,
        "message": "like increased successfully"
    }


######## UNLIKE POST ############
@router.put("/{update_id}/decreaseLike")
async def decrease_update_likes(update_id: str, user_id: str, response: Response):
    """
    PUT: increase Like
    """

    collection_id = "ClubUpdates"
    result = firebase_adapter.increment(
        collection_id, document_id=update_id, field="likes", value=-1)
    print(result)

    data = "likedBy:"
    result2 = firebase_adapter.remove_from_array(
        collection_id, update_id, "likedBy", user_id)
    print(result2)
    return {
        "status": 200,
        "message": "like decreased successfully"
    }


@router.get("/test-images")
async def get_images(response: Response):
    club_images = firebase_adapter.get_club_images()
    category_images = firebase_adapter.get_category_images()

    return {
        'clubImages': club_images,
        'categoryImages': category_images
    }


@router.get("/search/{club_name}")
async def get_club_id(club_name: str):
    query = """
        SELECT ClubID FROM Club WHERE ClubName LIKE %s
    """

    result = sql_adapter.query(query, ('%' + club_name + '%',))

    # Check if result exists
    if result:
        return {
            "message": "Successfully updated",
            "club_id": result[0][0]
        }
    else:
        return {
            "message": "Club not found"
        }
