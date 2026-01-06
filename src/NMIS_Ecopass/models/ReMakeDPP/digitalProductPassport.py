from pydantic import BaseModel,Field
from typing import Optional
from .metadata import Metadata
from .productIdentifier import ProductIdentifier
from .carbonFootprint import CarbonFootprint
from . circularity import Circularity
from .remanufacture import RepairModel
from .materialComposition import ProductMaterial
from .additionalData import AdditionalData
from pydantic import ConfigDict

class DigitalProductPassport(BaseModel):
    metadata: Metadata = Field(
        default_factory=Metadata,
        description="Passport metadata"
    )
    productIdentifier: ProductIdentifier = Field(
        default_factory=ProductIdentifier,
        description="Product identification"
    )
    circularity: Circularity = Field(
        default_factory=Circularity,
        description="Circularity information"
    )
    carbonFootprint: CarbonFootprint = Field(
        default_factory=CarbonFootprint,
        description="Carbon footprint data"
    )
    reManufacture: RepairModel = Field(
        default_factory=RepairModel,
        description="Remanufacturing data"
    )
    productMaterial: ProductMaterial = Field(
        default_factory=ProductMaterial,
        description="Material composition"
    )
    
    additionalData: Optional[AdditionalData] = Field(
        default=None,
        description="Optional additional custom data"
    )

    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
                "metadata": {
                    "backup_reference": "https://example.com/backup",
                    "registration_identifier": "https://example.com/registration/12345",
                    "economic_operator_id": "ECO-987654321",
                    "last_modification": "2024-08-27T14:30:00Z",
                    "predecessor": "https://example.com/registration/12344",
                    "issue_date": "2024-01-15T09:00:00Z",
                    "version": "1.2.3",
                    "passport_identifier": "123e4567-e89b-12d3-a456-426614174000",
                    "status": "active",
                    "expiration_date": "2025-01-15T09:00:00Z"
                },
                "productIdentifier": {
                    "batchID": "BCH-20240913-001",
                    "serialID": "SN-AB123456789",
                    "productStatus": "original"
                },
                "circularity": {
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
                },
                "carbonFootprint": {
                    "carbonFootprintPerLifecycleStage": [{
                        "lifecycleStage": "rawMaterial",
                        "carbonFootprint": 20.0
                    }],
                    "carbonFootprintStudy": "https://www.example.com/carbonstudy",
                    "productCarbonFootprint": 100.0,
                    "carbonFootprintPerformanceClass": "Carbon Trust label"
                },
                "reManufacture": {
                    "repairId": "REP-2024-001",
                    "currentCondition": "repairable",
                    "defects": [
                        {
                            "defectId": "DEF-001",
                            "description": "Tip wear",
                            "location": "blade_tip",
                            "dimensions": {"length": 25.0, "width": 3.0, "depth": 1.5},
                            "severity": 3,
                            "repairability": "repairable"
                        }
                    ],
                    "repairHistory": [
                        {
                            "repairId": "REP-2023-001",
                            "repairDate": "2023-06-15T10:00:00",
                            "repairType": "surfaceTreatment",
                            "facility": "NMIS Repair Center"
                        }
                    ],
                    "processSteps": [
                        {
                            "stepId": "STEP-001",
                            "processCategory": "inspection",
                            "processType": "materialAddition",
                            "parameters": {
                                "cleaningMethod": "ultrasonic",
                                "inspectionType": "visual_and_dimensional"
                            },
                            "startTime": "2024-02-01T09:00:00",
                            "endTime": "2024-02-01T11:00:00",
                            "operators": ["INSP-TECH-001"],
                            "documentation": ["https://nmis.scot/repairs/TB-2024-001/inspection.pdf"]
                        }
                    ],
                    "testResults": [
                        {
                            "testId": "TEST-001",
                            "testType": "penetrantInspection",
                            "parameters": {"penetrantType": "Type II"},
                            "results": {"indicationFound": False},
                            "conformity": True,
                            "date": "2024-02-02T10:00:00",
                            "personnel": "NDT-TECH-001"
                        }
                    ],
                    "approvals": {
                        "inspector": { "id": "INSP-001", "date": "2024-02-03T10:00:00"},
                        "supervisor": { "id": "SUP-001", "date": "2024-02-03T11:00:00"}
                    },
                    "certification": {
                        "certificateNumber": "CERT-2024-001",
                        "issueDate": "2024-02-03T12:00:00",
                        "documentUrl": "https://nmis.scot/certificates/REP-2024-001.pdf"
                    },
                    "nextMaintenanceDue": "2025-02-03T00:00:00",
                    "restrictions": [
                        "Maximum operating temperature: 1200°C",
                        "Inspection required after 5000 operating hours"
                    ],
                    "qifDocuments": [
                        {
                            "documentId": "QIF-2024-001",
                            "uri": "https://nmis.scot/qif/REP-2024-001/inspection.qif",
                            "hash": "a1b2c3d4e5f6...",
                            "timestamp": "2024-02-01T11:00:00"
                        }
                    ]
                },
                "materialInformation": {
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
                                    "unit": "weight_percent"
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
                },
                "additionalData": {
                    "data_type": "quality_metrics",
                    "data": {
                        "reliability_score": 95,
                        "performance_rating": "A+"
                    },
                    "url": "https://example.com/quality-docs",
                    "created_at": "2024-03-20T10:00:00",
                    "created_by": "QA_TEAM",
                    "description": "Quality assessment metrics"
                }
            }
        }
    )

