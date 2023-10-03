import os
import logging

# from config import conf
from fastapi import APIRouter, Cookie, Form, status, Body, Depends, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from config.firebase import Firebase
from config.constants import ADVERTISEMENT_COLLECTION, NOTICEBOARD_COLLECTION, UTILS_COLLECTION
from .exampleSchema import AdvertisementModel, AnalyticsModel, InteractionModel


logging.basicConfig(level=logging.INFO)
# ??? not working - to be investigated
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

router = APIRouter(
    prefix="/example",
    tags=['example']
)


auth_responses = {
    403: {"description": "Not enough privileges"},
}

# Initialize Firebase
crud = Firebase()


@router.get("/all")
async def all(response: Response):
    """
    GET: Fetch all the advertisements data for the overview screen and redux
    """

    result = crud.get('example')

    return {"message": "All advertisements data fetched successfully", "data": result}

# CRUD operations for single example


@router.get("/{advertisement_id}")
async def get_advertisement(advertisement_id: str, response: Response):
    """
    GET: Fetch a single example
    """

    return {"message": "example fetched successfully"}


@router.post("/")
async def add_advertisement(body: AdvertisementModel, response: Response):
    """
    POST: Add a new example
    """

    body = body.dict()
    ad_id = body['id']

    # Add example to example collection
    crud.add(collection_path=ADVERTISEMENT_COLLECTION,
             data=body, document_id=ad_id)

    return {"message": "example added successfully"}


@router.put("/{advertisement_id}")
async def update_advertisement(advertisement_id: str, response: Response):
    """
    PUT: Update a example
    """

    return {"message": "example updated successfully"}


@router.delete("/{advertisement_id}")
async def delete_advertisement(advertisement_id: str, response: Response):
    """
    DELETE: Delete a example
    """

    return {"message": "example deleted successfully"}


# Gets all noticeboard data based on advertisement_id
@router.get("/noticeboard/{advertisement_id}")
async def get_noticeboard(advertisement_id: str, response: Response):
    """
    GET: Fetch all the noticeboard data based on advertisement_id
    Tip: Just get all the documents from the example/ad-id/noticeboard collection
    """

    return {"message": "All noticeboard data fetched successfully"}

# Get top performing location of an example


@router.get("/top_location/{advertisement_id}")
async def get_top_location(advertisement_id: str, response: Response):
    """
    GET: Fetch top performing location of an example
    """

    return {"message": "Top performing location fetched successfully"}


# noticeboard/noticeboard-189182929/example/ad-2910182
