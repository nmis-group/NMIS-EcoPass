from pydantic import BaseModel, Field, HttpUrl,ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

class StatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"

class Metadata(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "backup_reference": "https://example.com/backup",
                "registration_identifier": "https://example.com/registration/12345",
                "economic_operator_id": "ECO-987654321",
                "last_modification": "2024-08-27T14:30:00Z",
                "predecessor": "https://example.com/registration/12344",
                "issue_date": "2024-01-15T09:00:00Z",
                "version": "1.2.3",
                "passport_identifier": "123e4567-e89b-12d3-a456-426614174000",
                "status": "active",
                "expiration_date": "2025-01-15T09:00:00Z"
            }
        }
    )
    
    backup_reference: Optional[HttpUrl] = Field(
        default=None, 
        description="Optional reference to a backup version of the DPP within a third party provider."
    )
    registration_identifier: Optional[HttpUrl] = Field(
        default=None, 
        description="URL back to EU Registry."
    )
    economic_operator_id: Optional[str] = Field(
        default=None,
        description="The identifier for the economic operator, typically a unique company ID, e.g., tax code"
    )
    last_modification: Optional[datetime] = Field(
        default=None,
        description="Timestamp of the last modification to the DPP."
    )
    predecessor: Optional[str] = Field(
        default=None, 
        description="Optional reference to the predecessor version of the DPP, if applicable."
    )
    issue_date: Optional[datetime] = Field(
        default=None,
        description="The date when the DPP was issued."
    )
    version: Optional[str] = Field(
        default=None, 
        description="This is for internal version of the DPP."
    )
    passport_identifier: Optional[UUID] = Field(
        default=None,
        description="A unique identifier for the digital product passport, uuid4."
    )
    status: StatusEnum = Field(
        default=None,
        description="The current status of the metadata, e.g., draft, active, inactive, expired."
    )
    expiration_date: Optional[datetime] = Field(
        default=None, 
        description="The date when the DPP will expire, usually required till end of product life - if applicable."
    )