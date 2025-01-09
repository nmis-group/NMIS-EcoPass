from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional, List, Dict,Any
from enum import Enum
from datetime import datetime
from .circularity import SupplierInformation,  RecycledContent

class MaterialCategory(str, Enum):
    METAL = "metal"
    POLYMER = "polymer"
    CERAMIC = "ceramic"
    COMPOSITE = "composite"
    SEMICONDUCTOR = "semiconductor"
    COATING = "coating"
    OTHER = "other"

class MaterialForm(str, Enum):
    SOLID = "solid"
    POWDER = "powder"
    LIQUID = "liquid"
    SHEET = "sheet"
    WIRE = "wire"
    BAR = "bar"
    TUBE = "tube"
    COATING = "coating"

class MaterialStandard(str, Enum):
    ASTM = "astm"
    ISO = "iso"
    EN = "en"
    JIS = "jis"
    AWS = "aws"
    CUSTOM = "custom"

class MaterialCertificationType(str, Enum):
    TYPE_2_1 = "EN10204_2.1"
    TYPE_2_2 = "EN10204_2.2"
    TYPE_3_1 = "EN10204_3.1"
    TYPE_3_2 = "EN10204_3.2"
    CUSTOM = "custom"

    @property
    def description(self) -> str:
        descriptions: Dict[str, str] = {
            "EN10204_2.1": "Certificate of Compliance - A document issued by the manufacturer confirming that the supplied products are in compliance with the order requirements",
            "EN10204_2.2": "Test Report - A document issued by the manufacturer in which they declare that the products delivered are in compliance with the requirements of the order and supply test results",
            "EN10204_3.1": "Inspection Certificate - Document issued by the manufacturer with test results from specific inspection on the delivered products",
            "EN10204_3.2": "Inspection Certificate with third party verification - Similar to 3.1 but with additional verification by an independent third party",
            "custom": "Custom certification type not covered by EN10204 standard"
        }
        return descriptions[self.value]

class MaterialProperty(BaseModel):
    propertyName: str = Field(
        description="Name of the material property"
    )
    value: float = Field(
        description="Numerical value of the property"
    )
    unit: str = Field(
        description="Unit of measurement"
    )
    testMethod: Optional[str] = Field(
        default=None,
        description="Test method used to determine property"
    )
    testConditions: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Test conditions under which property was measured"
    )

class MaterialComposition(BaseModel):
    element: str = Field(
        description="Chemical element or compound"
    )
    unit: str = Field(
        default="weight_percent",
        description="Percentage weight for composition"
    )

class MaterialCertification(BaseModel):
    certificationType: MaterialCertificationType = Field(
        description="Type of material certification"
    )
    certificateNumber: str = Field(
        description="Unique certificate identifier"
    )
    issuer: str = Field(
        description="Organization issuing the certificate"
    )
    issueDate: datetime = Field(
        description="Date of certificate issuance"
    )
    validUntil: Optional[datetime] = Field(
        default=None,
        description="Certificate validity period"
    )
    documentURL: HttpUrl = Field(
        description="URL to certification document"
    )

class MaterialTraceability(BaseModel):
    batchNumber: str = Field(
        description="Material batch or heat number"
    )

class MaterialSustainability(BaseModel):
    carbonFootprint: Optional[float] = Field(
        default=None,
        description="Carbon footprint per kg of material"
    )
    environmentalLabels: Optional[List[str]] = Field(
        default=None,
        description="Environmental certifications"
    )
    circularityReference: Optional[str] = Field(
        default=None,
        description="Reference to circularity data containing recycling and disposal info"
    )

class MaterialInformation(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "materialId": "MAT-2024-001",
                "tradeName": "Inconel 718",
                "materialCategory": "metal",
                "materialStandard": "astm",
                "standardDesignation": "ASTM B637",
                "composition": [
                    {
                        "element": "Ni",
                        "minimum": 50.0,
                        "maximum": 55.0,
                        "actual": 52.3
                    }
                ],
                "materialForm": "bar",
                "properties": [
                    {
                        "propertyName": "tensileStrength",
                        "value": 1375.0,
                        "unit": "MPa"
                    }
                ]
            }
        }
    )

    materialId: str = Field(
        description="Unique identifier for material"
    )
    tradeName: str = Field(
        description="Commercial or trade name"
    )
    materialCategory: MaterialCategory = Field(
        description="Basic category of material"
    )
    materialStandard: MaterialStandard = Field(
        description="Governing material standard"
    )
    standardDesignation: str = Field(
        description="Standard material designation"
    )
    composition: List[MaterialComposition] = Field(
        description="Chemical composition details"
    )
    materialForm: MaterialForm = Field(
        description="Physical form of material"
    )
    properties: List[MaterialProperty] = Field(
        description="Material properties"
    )
    certifications: Optional[List[MaterialCertification]] = Field(
        default=None,
        description="Material certifications"
    )
    traceability: MaterialTraceability = Field(
        description="Material traceability information"
    )
    sustainability: Optional[MaterialSustainability] = Field(
        default=None,
        description="Sustainability information"
    )
    processingGuidelines: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Guidelines for material processing"
    )
    safetyDataSheet: Optional[HttpUrl] = Field(
        default=None,
        description="Link to material safety data sheet"
    )
    applicableStandards: Optional[List[str]] = Field(
        default=None,
        description="Additional applicable standards"
    )
    documentation: Optional[Dict[str, HttpUrl]] = Field(
        default=None,
        description="Additional documentation links"
    )

class ProductMaterial(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "productId": "PROD-2024-001",
                "components": {
                    "housing": {
                        "materialId": "MAT-2024-001",
                        "tradeName": "Aluminum 6061-T6",
                        "materialCategory": "metal",
                        "materialStandard": "astm",
                        "standardDesignation": "ASTM B209",
                        "composition": [
                            {
                                "element": "Al",
                                "unit": "weight_percent",
                            }
                        ],
                        "properties": [
                            {
                                "propertyName": "tensileStrength",
                                "value": 310.0,
                                "unit": "MPa"
                            }
                        ],
                        "traceability": {
                            "batchNumber": "BATCH-001"
                        }
                    }
                },
                "totalMass": 2.5,
                "materialBreakdown": {
                    "aluminum": 85.0,
                    "steel": 15.0
                },
                "recycledContentTotal": 30.5,
                "hazardousMaterials": ["chromium_coating"],
                "circularityReference": "example.com/circularity-id"
            }
        }
    )
    productId: str = Field(
        description="Reference to product identifier"
    )
    components: Dict[str, MaterialInformation] = Field(
        description="Map of component names to their materials"
    )
    totalMass: float = Field(
        description="Total mass of product in kg"
    )
    materialBreakdown: Dict[str, float] = Field(
        description="Percentage breakdown of materials by mass"
    )
    recycledContentTotal: Optional[float] = Field(
        default=None,
        description="Total percentage of recycled content"
    )
    hazardousMaterials: Optional[List[str]] = Field(
        default=None,
        description="List of any hazardous materials"
    )
    circularityReference: Optional[str] = Field(
        default=None,
        description="Reference to circularity data URL"
    )