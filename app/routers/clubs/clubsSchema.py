from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime


class ClubUpdateSchema(BaseModel):
    ctaLink: str | None = None
    id: str
    media: str | None = None
    message: str
    postType: str
    public: bool


class ClubProfileSchema(BaseModel):
    email: str
    description: str
    instagram: str
    location: str
    training: str


# Look at the examples directory for more examples
