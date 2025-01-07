from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class AdditionalData(BaseModel):
    """
    Pydantic model for storing additional DPP data with flexible structure
    """
    data_type: str = Field(
        ...,
        description="Identifier for the type of additional data",
        max_length=100
    )
    
    data: Dict[str, Any] = Field(
        ...,
        description="Additional data stored in dictionary format"
    )
    
    url: Optional[HttpUrl] = Field(
        None,
        description="URL reference to external resource or documentation"
    )
    
    # Metadata fields
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = Field(
        None,
        description="Username or ID of the creator"
    )
    
    # Optional reference fields
    reference_id: Optional[str] = Field(
        None,
        description="ID reference to related object",
        max_length=255
    )
    reference_model: Optional[str] = Field(
        None,
        description="Name of the related model",
        max_length=100
    )
    
    description: Optional[str] = Field(
        None,
        description="Description of the additional data"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "data_type": "environmental_impact",
                "data": {
                    "carbon_footprint": 125.5,
                    "waste_reduction": "30%",
                    "renewable_energy_usage": {
                        "solar": "40%",
                        "wind": "20%"
                    }
                },
                "url": "https://example.com/documentation",
                "reference_id": "123",
                "reference_model": "Product",
                "description": "Environmental impact metrics for product 123"
            }
        }