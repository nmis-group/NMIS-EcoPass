from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List, Annotated
from enum import Enum
from uuid import UUID

class DocumentType(str, Enum):
    BILLOFMATERIAL = "billOfMaterial"
    MODEL3D = "model3d"
    DISMANTLINGMANUAL = "dismantlingManual"
    REMANUFACTUREMANUAL = "remanufactureManual"
    REPAIRMANUAL="repairManual"
    DRAWING="drawing"
    OTHERMANUAL="otherManual"

class MimeType(str,Enum):
    PDF = "application/pdf"
    JSON = "application/json"
    JPEG = "image/jpeg"
    PNG = "image/png"
    HTML = "text/html"
    XML = "application/xml"
    CSV = "text/csv"

    # 3D Model MIME types
    GLTF_JSON = "model/gltf+json"
    GLTF_BINARY = "model/gltf-binary"
    STL = "model/stl"
    STEP = "application/step"

class ResourcePath(BaseModel):
    resourcePath: HttpUrl = Field(
        ..., 
        description="The resource path to your document or supplier web address. Eg example.com/example.step"
    )

class DismantlingAndRemovalDocumentation(BaseModel):
    documentType: DocumentType = Field(
        ..., 
        description="Describes type for document e.g. 'Dismantling manual'")
    mimeType: MimeType = Field(
        ...,
        description="Defines internet media type to determine how to interpret the document URL")
    documentURL: ResourcePath = Field(
        ...,
        description="Link to document")


class SetOfDocumentation(BaseModel):
    __root__: List[DismantlingAndRemovalDocumentation] = Field(
        ...,
        description="A set of required documentation to support End of life actions")

class PerConsumerWasteRecycled(BaseModel):
    preConsumerWasteRecycled:Annotated[float, Field(strict=True, gt=0, le=100)]= Field(
        ...,
        description="Percentage amount of waste material recycled during production of product"
    )

class PostConsumerWasteRecycled(BaseModel):
    postConsumerWasteRecycled:Annotated[float, Field(strict=True, gt=0, le=100)]= Field(
        ...,
        description="Percentage amount of waste material recycled from post consumer waste"
    )

class RecycledMaterial(str, Enum):
    ALUMINUM = "Aluminum"
    STEEL = "Steel"
    PLASTIC = "Plastic"
    COPPER = "Copper"
    LITHIUM = "Lithium"
    COBALT = "Cobalt"
    NICKEL = "Nickel"
    TITANIUM="Titanium"

class RecycledMaterialInfo(BaseModel):
    material: RecycledMaterial = Field(
        ...,
        description="The type of recycled material used.")
    materialInfoURL: HttpUrl = Field(
        ...,
        description="A URL linking to information about this material, such as material properties, alloy information, etc.")

class RecycledContent(BaseModel):
    preConsumerShare: PerConsumerWasteRecycled = Field(..., description="Pre-consumer waste share")
    recycledMaterial: RecycledMaterialInfo = Field(..., description="Type of recycled material")
    postConsumerShare: PostConsumerWasteRecycled = Field(..., description="Post-consumer waste share")

class RecycledContentSet(BaseModel):
    __root__: List[RecycledContent] = Field(..., uniqueItems=True)


class EndOfLifeInformationEntity(BaseModel):
    wastePrevention: ResourcePath = Field(..., description="Information on waste prevention")
    separateCollection: ResourcePath = Field(..., description="Information on separate collection")
    informationOnCollection: ResourcePath = Field(..., description="Information on collection points")

class EndOfLifeInformation(EndOfLifeInformationEntity):
    pass

class AddressOfSupplier(BaseModel):
    addressCountry: str = Field(..., description="Country of the address")
    postalCode: str = Field(..., description="Postal code")
    streetAddress: str = Field(..., description="Street address")

class SupplierInformation(BaseModel):
    name:str = Field(
        ...,
        description="Supplier Name"
    )
    address:AddressOfSupplier = Field(
        ...,
        description="Address of supplier"
    )
    email : EmailStr = Field(
        ...,
        description="Supplier email address"
    )
    supplierWebaddress: ResourcePath = Field(
        ...,
        description="Supplier website address if available"
    )


class Circularity(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "dismantlingAndRemovalInformation"
            }
        }
    )
    
    dismantlingAndRemovalInformation: Optional[SetOfDocumentation] = Field(
        default=None, 
        description="Dismantling, Repair and removal information to customer"
    )

    recycledContent:Optional[RecycledContentSet]=Field(
        ...,
        description="Share of recycled material"
    )
    endOfLifeInformation:Optional[EndOfLifeInformation]=Field(
        ...,
        description="End of life Information"
    )
    supplierInformation:Optional[SupplierInformation]=Field(
        ...,
        description="Suppliers who could support with spares and end of life support"
    )

