from pydantic import BaseModel, Field, HttpUrl, RootModel, ConfigDict, EmailStr
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
        default=None, 
        description="The resource path to your document or supplier web address. Eg example.com/example.step"
    )

class DismantlingAndRemovalDocumentation(BaseModel):
    documentType: DocumentType = Field(
        default=None, 
        description="Describes type for document e.g. 'Dismantling manual'")
    mimeType: MimeType = Field(
        default=None,
        description="Defines internet media type to determine how to interpret the document URL")
    documentURL: ResourcePath = Field(
        default=None,
        description="Link to document")


class SetOfDocumentation(BaseModel):
    RootModel: List[DismantlingAndRemovalDocumentation] = Field(
        default=None,
        description="A set of required documentation to support End of life actions")

class PerConsumerWasteRecycled(BaseModel):
    preConsumerWasteRecycled:Annotated[float, Field(strict=True, gt=0, le=100)]= Field(
        default=None,
        description="Percentage amount of waste material recycled during production of product"
    )

class PostConsumerWasteRecycled(BaseModel):
    postConsumerWasteRecycled:Annotated[float, Field(strict=True, gt=0, le=100)]= Field(
        default=None,
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
        default=None,
        description="The type of recycled material used.")
    materialInfoURL: HttpUrl = Field(
        default=None,
        description="A URL linking to information about this material, such as material properties, alloy information, etc.")

class RecycledContent(BaseModel):
    preConsumerShare: PerConsumerWasteRecycled = Field(default=None, description="Pre-consumer waste share")
    recycledMaterial: RecycledMaterialInfo = Field(default=None, description="Type of recycled material")
    postConsumerShare: PostConsumerWasteRecycled = Field(default=None, description="Post-consumer waste share")

class RecycledContentSet(BaseModel):
    RootModel: List[RecycledContent] = Field(default=None, uniqueItems=True)


class EndOfLifeInformationEntity(BaseModel):
    wastePrevention: ResourcePath = Field(default=None, description="Information on waste prevention")
    separateCollection: ResourcePath = Field(default=None, description="Information on separate collection")
    informationOnCollection: ResourcePath = Field(default=None, description="Information on collection points")

class EndOfLifeInformation(EndOfLifeInformationEntity):
    pass

class AddressOfSupplier(BaseModel):
    addressCountry: str = Field(default=None, description="Country of the address")
    postalCode: str = Field(default=None, description="Postal code")
    streetAddress: str = Field(default=None, description="Street address")

class SupplierInformation(BaseModel):
    name:str = Field(
        default=None,
        description="Supplier Name"
    )
    address:AddressOfSupplier = Field(
        default=None,
        description="Address of supplier"
    )
    email : EmailStr = Field(
        default=None,
        description="Supplier email address"
    )
    supplierWebaddress: ResourcePath = Field(
        default=None,
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
        default=None,
        description="Share of recycled material"
    )
    endOfLifeInformation:Optional[EndOfLifeInformation]=Field(
        default=None,
        description="End of life Information"
    )
    supplierInformation:Optional[SupplierInformation]=Field(
        default=None,
        description="Suppliers who could support with spares and end of life support"
    )

