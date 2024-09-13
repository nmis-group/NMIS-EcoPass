from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional,List
from enum import Enum

class LifecycleStage(str, Enum):
    RAWMATERIALEXTRACTION = "rawMaterial"
    SUPPLYCHAIN = "supplyChain"
    MAINPRODUCTION = "mainProduction"
    DISTRIBUTION = "distribution"
    RECYCLING = "recycling"
    REMANUFACTURE="remanufacture"

class LifecycleStageCarbonFootprint(BaseModel):
    lifecycleStage: LifecycleStage = Field(
        ..., 
        description="The stage of the product's lifecycle"
    )
    carbonFootprint: float = Field(
        ..., 
        description="Carbon footprint associated with this lifecycle stage in Kilograms"
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
    carbonFootprintPerLifecycleStage: Optional[List[LifecycleStageCarbonFootprint]] = Field(
        ..., 
        description="List of carbon footprints associated with each stage of the product's lifecycle"
    )
    carbonFootprintStudy: Optional[HttpUrl] = Field(
        ..., 
        description="URL to the carbon footprint study or related document"
    )
    productCarbonFootprint: Optional[float] = Field(
        ..., 
        description="Carbon footprint associated with the battery component of the product"
    )
    carbonFootprintPerformanceClass: Optional[str] = Field(
        ..., 
        description="Performance class of the product based on its carbon footprint"
    )
