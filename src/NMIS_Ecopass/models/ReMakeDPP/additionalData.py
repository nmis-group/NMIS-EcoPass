from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class AdditionalData(BaseModel):
    """
    Additional DPP data with flexible structure
    """
    data_type: str = Field(
        ...,
        description="Identifier for the type of additional data",
        max_length=100,
        example="environmental_impact"
    )
    
    data: Dict[str, Any] = Field(
        ...,
        description="Additional data stored in dictionary format",
        example={
            "carbon_footprint": 125.5,
            "waste_reduction": "30%",
            "renewable_energy_usage": {
                "solar": "40%",
                "wind": "20%"
            }
        }
    )
    
    url: Optional[HttpUrl] = Field(
        None,
        description="URL reference to external resource or documentation",
        example="https://example.com/environmental-impact/doc-123"
    )
    
    # Metadata fields
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = Field(
        None,
        description="Username or ID of the creator or email address"
    )
    reference_model: Optional[HttpUrl] = Field(
        None,
        description="URL reference to documentation explaining the data model or schema",
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
                "url": "https://company-name.com/documentation",
                "created_at": "2024-03-20T10:00:00",
                "created_by": "company_name@email.com",
                "reference_model": "https://company-name.com/schemas/product",
                "description": "Environmental impact metrics for product 123"
            }
        }