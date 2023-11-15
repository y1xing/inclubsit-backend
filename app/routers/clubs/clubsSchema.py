from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime

class ClubUpdateSchema(BaseModel):
    ctaLink : str
    id: str
    media : str
    message: str
    postType : str
    public : bool

class ClubProfileSchema(BaseModel):
    ClubName: str
    ClubDescription: str



# Look at the examples directory for more examples