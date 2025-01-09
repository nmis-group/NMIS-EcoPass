from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional, List, Annotated, Union
from enum import Enum


class DocumentType(str, Enum):
    BILLOFMATERIAL = "billOfMaterial"
    MODEL3D = "model3d"
    DISMANTLINGMANUAL = "dismantlingManual"
    REMANUFACTUREMANUAL = "remanufactureManual"
    REPAIRMANUAL = "repairManual"
    DRAWING = "drawing"
    OTHERMANUAL = "otherManual"



class MimeType(str, Enum):
    PDF = "application/pdf"
    JSON = "application/json"
    JPEG = "image/jpeg"
    PNG = "image/png"
    HTML = "text/html"
    XML = "application/xml"
    CSV = "text/csv"
    QIF = "application/qif"
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



class PerConsumerWasteRecycled(BaseModel):
    preConsumerWasteRecycled: Annotated[float, Field( gt=0, le=100)] = Field(
        default=None,
        description="Percentage amount of waste material recycled during production of product"
    )


class PostConsumerWasteRecycled(BaseModel):
    postConsumerWasteRecycled: Annotated[float, Field(gt=0, le=100)] = Field(
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
    TITANIUM = "Titanium"
    OTHER = "Other"


class RecycledMaterialInfo(BaseModel):
    material: RecycledMaterial = Field(
        default=None,
        description="The type of recycled material used within the product.")
    materialInfoURL: HttpUrl = Field(
        default=None,
        description="A URL linking to information about the recycled material, such as material properties, alloy information, etc.")


class RecycledContent(BaseModel):
    preConsumerShare: Annotated[float, Field(gt=0, le=100)] = Field(
        default=None, description="Pre-consumer waste recycled percentage")
    recycledMaterial: RecycledMaterialInfo = Field(
        default=None, description="Type of recycled material")
    postConsumerShare: Annotated[float, Field(gt=0, le=100)] = Field(
        default=0.0, description="Post-consumer waste recycled percentage")



class EndOfLifeInformationEntity(BaseModel):
    wastePrevention: ResourcePath = Field(
        default=None, description="Information on waste prevention")
    separateCollection: ResourcePath = Field(
        default=None, description="Information on separate collection")
    informationOnCollection: ResourcePath = Field(
        default=None, description="Information on collection points")


class EndOfLifeInformation(EndOfLifeInformationEntity):
    pass


class AddressOfSupplier(BaseModel):
    addressCountry: str = Field(
        default=None, description="Country of the address")
    postalCode: str = Field(default=None, description="Postal code")
    streetAddress: str = Field(default=None, description="Street address")


class SupplierInformation(BaseModel):
    name: str = Field(
        default=None,
        description="Supplier who can provide spares and end of life support"
    )
    address: AddressOfSupplier = Field(
        default=None,
        description="Address of supplier"
    )
    email: str = Field(
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
                "dismantlingAndRemovalInformation": [
                    {
                        "documentType": "dismantlingManual",
                        "mimeType": "application/pdf",
                        "documentURL": {
                            "resourcePath": "https://example.com/documents/dismantling-manual.pdf"
                        }
                    },
                    {
                        "documentType": "repairManual",
                        "mimeType": "text/html",
                        "documentURL": {
                            "resourcePath": "https://example.com/documents/repair-manual.html"
                        }
                    }
                ],
                "recycledContent": [
                    {
                        "preConsumerShare": 45.0,
                        "recycledMaterial": {
                            "material": "Aluminum",
                            "materialInfoURL": "https://example.com/materials/aluminum-info"
                        },
                        "postConsumerShare": 30.0
                    },
                    {
                        "preConsumerShare": 60.0,
                        "recycledMaterial": {
                            "material": "Plastic",
                            "materialInfoURL": "https://example.com/materials/plastic-info"
                        },
                        "postConsumerShare": 40.0
                    }
                ],
                "endOfLifeInformation": {
                    "wastePrevention": {
                        "resourcePath": "https://example.com/waste-prevention"
                    },
                    "separateCollection": {
                        "resourcePath": "https://example.com/separate-collection"
                    },
                    "informationOnCollection": {
                        "resourcePath": "https://example.com/collection-points"
                    }
                },
                "supplierInformation": {
                    "name": "Eco Parts Ltd.",
                    "address": {
                        "addressCountry": "Germany",
                        "postalCode": "DE-10719",
                        "streetAddress": "Kurfürstendamm 21"
                    },
                    "email": "contact@ecopartsltd.com",
                    "supplierWebaddress": {
                        "resourcePath": "https://ecopartsltd.com"
                    }
                }
            }

        }
    )

    dismantlingAndRemovalInformation: Optional[Union[DismantlingAndRemovalDocumentation, List[DismantlingAndRemovalDocumentation]]] = Field(
        default=None,
        description="Dismantling, Repair and removal information to customer"
    )

    recycledContent:Optional[Union[RecycledContent, List[RecycledContent]]] = Field(
        default=None,
        description="Share of recycled material"
    )
    endOfLifeInformation: Optional[EndOfLifeInformation] = Field(
        default=None,
        description="End of life Information"
    )
    supplierInformation: Optional[Union[SupplierInformation, List[SupplierInformation]]] = Field(
        default=None,
        description="Suppliers who could support with spares and end of life support"
    )
