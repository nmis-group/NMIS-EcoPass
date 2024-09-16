from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class ProductStatus(str, Enum):
    ORIGINAL = "original"
    REPAIRED = "repaired"
    MAINTAINED = "maintained"
    REMANUFACTURED = "remanufactured"
    RECYCLED = "recycled"


class ProductIdentifier(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "batchID": "BCH-20240913-001",
                "serialID":"SN-AB123456789",
                "productStatus":"original"

            }
        }
    )
    batchID: Optional[str] = Field(
        default=None, 
        description="Batch ID of products that were manufactured under similar conditions"
    )
    serialID: Optional[str] = Field(
        default=None, 
        description="Unique identifier assigned to the product"
    )
    productStatus: ProductStatus = Field(
        default=None,
        description="The current status of the product, e.g., original, maintained, repaired, remanufactured or recycled"
    )


#TODO: Need to add warranty, lifeExpectency of product, gross volume and other parameters