from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, List
from enum import Enum


class LifecycleStage(str, Enum):
    RAWMATERIALEXTRACTION = "rawMaterial"
    SUPPLYCHAIN = "supplyChain"
    MAINPRODUCTION = "mainProduction"
    DISTRIBUTION = "distribution"
    RECYCLING = "recycling"
    REMANUFACTURE = "remanufacture"


class LifecycleStageCarbonFootprint(BaseModel):
    lifecycleStage: LifecycleStage = Field(
        default=None,
        description="The stage of the product's lifecycle",
        example="mainProduction"
    )
    carbonFootprint: float = Field(
        default=None,
        description="Carbon footprint associated with this lifecycle stage in Kilograms",
        example=20.5
    )


class CarbonFootprint(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "carbonFootprintPerLifecycleStage":[{
                    "lifecyleStage":"rawMaterial",
                    "carbonFootprint":20.0
                }],
                "carbonFootprintStudy":"https://www.example.com/carbonstudy",
                "productCarbonFootprint":100.0,
                "carbonFootprintPerformanceClass":"Carbon Trust label"

            }
        }
    )
    carbonFootprintPerLifecycleStage: Optional[
        List[LifecycleStageCarbonFootprint]] = Field(
        default=None,
        description="List of carbon footprints associated with each stage of "
                    "the product's lifecycle"
    )
    carbonFootprintStudy: Optional[HttpUrl] = Field(
        default=None,
        description="URL to the carbon footprint study or related document"
    )
    productCarbonFootprint: Optional[float] = Field(
        default=None,
        description="Carbon footprint associated with the battery component of "
                    "the product"
    )
    carbonFootprintPerformanceClass: Optional[str] = Field(
        default=None,
        description="Performance class of the product based on its carbon "
                    "footprint"
    )
