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
                "productStatus":"original",
                "productName":"NMIS reference product",
                "productDescription":"A test product for DPP"

            }
        }
    )
    batchID: Optional[str] = Field(
        default=None, 
        description="Batch ID of products that were manufactured under similar conditions",
        example="BCH-20240913-001"
    )
    serialID: Optional[str] = Field(
        default=None, 
        description="Unique identifier assigned to the product",
        example="SN-AB123456789"
    )
    productStatus: ProductStatus = Field(
        default=None,
        description="The current status of the product, e.g., original, maintained, repaired, remanufactured or recycled",
        example="original"
    )
    productName: Optional[str] = Field(
        default=None,
        description="The name of the product",
        example="Product Name"
    )
    productDescription: Optional[str] = Field(
        default=None,
        description="A description of the product",
        example="A description of the product"
    )


#TODO: Need to add warranty, lifeExpectency of product, gross volume and other parameters