from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional, List, Dict, Union, Any
from enum import Enum
from datetime import datetime

class RepairType(str, Enum):
    MATERIAL_ADDITION = "materialAddition"
    MATERIAL_REMOVAL = "materialRemoval"
    SURFACE_TREATMENT = "surfaceTreatment"
    COMPONENT_REPLACE = "componentReplace"
    CLEANING = "cleaning"
    REASSEMBLY = "reassembly"
    ADJUSTMENT = "adjustment"
    HYBRID = "hybrid"

class ProcessCategory(str, Enum):
    INSPECTION = "inspection"
    DISASSEMBLY = "disassembly"
    REPAIR = "repair"
    TESTING = "testing"
    ASSEMBLY = "assembly"
    VALIDATION = "validation"
    CERTIFICATION = "certification"

class ComponentCondition(str, Enum):
    SERVICEABLE = "serviceable"
    REPAIRABLE = "repairable"
    REPAIRABLE_WITH_RESTRICTIONS = "repairableWithRestrictions"
    BEYOND_REPAIR = "beyondRepair"
    UNKNOWN = "unknown"

class ProcessStep(BaseModel):
    stepId: str = Field(
        description="Unique identifier for process step"
    )
    processCategory: ProcessCategory = Field(
        description="Category of process step"
    )
    processType: RepairType = Field(
        description="Type of repair process"
    )
    parameters: Dict[str, Any] = Field(
        description="Process-specific parameters and values"
    )
    startTime: datetime = Field(
        description="Process step start time"
    )
    endTime: datetime = Field(
        description="Process step completion time"
    )
    operators: List[str] = Field(
        description="Qualified operators performing step"
    )
    documentation: List[HttpUrl] = Field(
        description="Links to process documentation"
    )

class DefectInformation(BaseModel):
    defectId: str = Field(
        description="Unique defect identifier"
    )
    description: str = Field(
        description="Description of defect"
    )
    location: str = Field(
        description="Defect location on component"
    )
    dimensions: Dict[str, float] = Field(
        description="Measured dimensions of defect"
    )
    severity: int = Field(
        ge=1, le=5,
        description="Severity rating"
    )
    repairability: ComponentCondition = Field(
        description="Assessment of repairability"
    )

class TestResult(BaseModel):
    testId: str = Field(
        description="Unique test identifier"
    )
    testType: str = Field(
        description="Type of test performed"
    )
    parameters: Dict[str, Any] = Field(
        description="Test parameters"
    )
    results: Dict[str, Any] = Field(
        description="Test results"
    )
    conformity: bool = Field(
        description="Whether results meet specifications"
    )
    date: datetime = Field(
        description="Test date"
    )
    personnel: str = Field(
        description="Testing personnel"
    )

class QIFDocument(BaseModel):
    documentId: str = Field(description="QIF document identifier")
    uri: HttpUrl = Field(description="URI to QIF document location")
    hash: str = Field(description="SHA-256 hash of QIF document")
    timestamp: datetime = Field(description="Document creation/update timestamp")

    
class RepairHistory(BaseModel):
    repairId: str = Field(
        description="Reference to previous repair"
    )
    repairDate: datetime = Field(
        description="Date of repair"
    )
    repairType: RepairType = Field(
        description="Type of repair performed"
    )
    facility: str = Field(
        description="Facility where repair was performed"
    )

class RepairModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        json_schema_extra={
            "example": {
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
                    "inspector": {"name": "John Smith", "id": "INSP-001", "date": "2024-02-03T10:00:00"},
                    "supervisor": {"name": "Jane Doe", "id": "SUP-001", "date": "2024-02-03T11:00:00"}
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
            }
        }
    )

    repairId: str = Field(
        description="Unique repair identifier"
    )
    currentCondition: ComponentCondition = Field(
        description="Current condition assessment"
    )
    defects: Optional[List[DefectInformation]] = Field(
        default=None,
        description="Identified defects"
    )
    repairHistory: Optional[List[RepairHistory]] = Field(
        default=None,
        description="History of previous repairs"
    )
    processSteps: Optional[List[ProcessStep]] = Field(
        default=None,
        description="Repair process steps"
    )
    testResults: Optional[List[TestResult]] = Field(
        default=None,
        description="Test results"
    )
    approvals: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Required approval signatures"
    )
    certification: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Certification information - url to certification document"
    )
    nextMaintenanceDue: Optional[datetime] = Field(
        default=None,
        description="Next maintenance due date"
    )
    restrictions: Optional[List[str]] = Field(
        default=None,
        description="Post-repair operational restrictions"
    )
    qifDocuments: Optional[List[QIFDocument]] = Field(
        default=[],
        description="List of associated QIF documents"
    )