from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime

#### SUB-SCHEMAS ####
class OrganisationModel(BaseModel):
    name: str
    email: str
    contact: str

    class Config:
        json_schema_extra = {
            "name": "Example Organization",
            "email": "contact@example.org",
            "contact": "+1 (123) 456-7890"
        }

class AdvertisementDetailsModel(BaseModel):
    category: str
    startDate: datetime
    endDate: datetime
    tags: list[str]

    class Config:
        json_schema_extra = {
            "category": "Fashion",
            "startDate": "2023-09-15T00:00:00Z",
            "endDate": "2023-09-30T23:59:59Z",
            "tags": ["Sale", "Discount"]
        }

class AnalyticsModel(BaseModel):
    views: int
    clicks: int

    class Config:
        json_schema_extra = {
            "views": 1000,
            "clicks": 50
        }

class CtaModel(BaseModel):
    link: str
    purpose: str

    class Config:
        json_schema_extra = {
            "link": "https://example.com/cta",
            "purpose": "Learn More"
        }

class TargetAudienceModel(BaseModel):
    ageRange: list[str] | None = None
    district: list[str] | None = None
    targetTiming: list[str] | None = None

    class Config:
        json_schema_extra = {
            "ageRange": ["18-35", "36-50"],
            "district": ["Downtown", "Suburb"],
            "targetTiming": ["Morning", "Evening"]
        }


#### MAIN SCHEMA ####
class AdvertisementModel(BaseModel):
    id: str
    title: str
    description: str
    image: str
    status: str
    organisation: OrganisationModel
    details: AdvertisementDetailsModel
    cta: CtaModel
    targetAudience: TargetAudienceModel
    comments: str
    analytics: AnalyticsModel

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234567890",
                "title": "Sample Advertisement",
                "description": "This is a sample example description.",
                "image": "https://firebasestorage.googleapis.com/v0/b/bts-cms.appspot.com/o/2.png?alt=media&token=e9b23fed-4dd8-4091-b497-ef9eabe76db4",
                "status": "Active",
                "organisation": {
                    "name": "Example Organization",
                    "email": "contact@example.org",
                    "contact": "+65 1234 5678"
                },
                "details": {
                    "category": "Fashion",
                    "startDate": "2023-09-15T00:00:00Z",
                    "endDate": "2023-09-30T23:59:59Z",
                    "tags": ["Sale", "Discount"]
                },
                "cta": {
                    "link": "https://www.google.com/",
                    "purpose": "Sign Up"
                },
                "targetAudience": {
                    "ageRange": ["18-35", "36-50"],
                    "district": ["PUNGGOL", "CHOA CHU KANG"],
                    "targetTiming": ["11:00 - 14:00"]
                },
                "comments": "No special comments.",
                "analytics": {
                    "views": 0,
                    "clicks": 0
                }
            }
        }


class InteractionModel(BaseModel):
    timestamp: datetime
    action: str

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2023-09-14T14:30:00.000Z",
                "action": "viewed"
            }
        }
