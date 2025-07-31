from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
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
        description="Unique identifier for process step",
        example="STEP-2024-001"
    )
    processCategory: ProcessCategory = Field(
        description="Category of process step (e.g., inspection, repair, testing)",
        example="inspection"
    )
    processType: RepairType = Field(
        description="Type of repair process (e.g., materialAddition, cleaning)",
        example="materialAddition"
    )
    parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Process-specific parameters and values",
        example={
            "temperature": 200,
            "pressure": 50,
            "duration": 30,
            "method": "laser_cladding"
        }
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
    documentation: List[str] = Field(
        description="Links to process documentation"
    )

class DefectInformation(BaseModel):
    defectId: str = Field(
        description="Unique defect identifier (format: DEF-YYYY-XXX)",
        example="DEF-2024-001"
    )
    description: str = Field(
        description="Detailed description of the defect including type and characteristics",
        example="Surface crack on leading edge, approximately 5mm in length"
    )
    location: str = Field(
        description="Specific location of defect on component using standard reference points",
        example="Leading edge, 50mm from root, pressure side"
    )
    dimensions: Dict[str, float] = Field(
        description="Measured dimensions of defect in millimeters",
        example={"length": 5.0, "width": 0.5, "depth": 2.0}
    )
    severity: int = Field(
        ge=1, le=5,
        description="Severity rating"
    )

class TestResult(BaseModel):
    testId: str = Field(
        description="Unique test identifier (format: TEST-YYYY-XXX)",
        example="TEST-2024-001"
    )
    testType: str = Field(
        description="Type of test performed (e.g., NDT, dimensional, performance)",
        example="fluorescent_penetrant_inspection"
    )
    parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Test parameters including equipment settings and environmental conditions",
        example={
            "penetrantType": "Type II",
            "developmentTime": 20,
            "temperature": 23.5,
            "humidity": 45
        }
    )
    results: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Test results"
    )
    conformity: Optional[bool] = Field(
        default=None,
        description="Whether results meet specifications"
    )
    date: Optional[datetime] = Field(
        default=None,
        description="Test date"
    )
    personnel: Optional[str] = Field(
        default=None,
        description="Testing personnel"
    )
    testResults: Optional[List[str]] = Field(
        default=None,
        description="Links to test results"
    )

class QIFDocument(BaseModel):
    documentId: str = Field(
        description="QIF document identifier (format: QIF-YYYY-XXX)",
        example="QIF-2024-001"
    )
    version: int = Field(
        default=1,
        description="Version number of the QIF document",
        ge=1
    )
    storage_path: str = Field(
        description="Storage path for the QIF document (format: qif/{documentId}/v{version}/measurement.qif)",
        example="qif/QIF-2024-001/v1/measurement.qif"
    )
    uri: str = Field(
        description="URI to QIF document location (HTTPS URL)",
        example="https://nmis.scot/qif/QIF-2024-001/v1/measurement.qif"
    )
    hash: str = Field(description="SHA-256 hash of QIF document")
    timestamp: datetime = Field(description="Document creation/update timestamp")

    
class RepairHistory(BaseModel):
    repairId: str = Field(
        description="Reference to previous repair (format: REP-YYYY-XXX)",
        example="REP-2023-001"
    )
    repairDate: datetime = Field(
        description="Date and time when repair was completed (ISO format)",
        example="2023-06-15T10:00:00"
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
                ],
                "defectManagement": "https://nmis.scot/docs/defect-management-bpmn.pdf",
                "remanufactureCostModel": "CostModel.xlsx",
                "remanufactureDESModel": "https://github.com/nmis/remanufacture-des-model",
                "remanufactureSkills": "https://nmis.scot/docs/skills-matrix.xlsx",
                "remanufactureEquipment": "https://nmis.scot/docs/equipment-list.docx",
                "remanufactureCertification": "https://nmis.scot/docs/certification.pdf",
                "remanufactureRepairId": "REP-2024-001"
            }
        }
    )

    repairId: Optional[str] = Field(
        default=None,
        description="Unique repair identifier (format: REP-YYYY-XXX)",
        example="REP-2024-001"
    )
    currentCondition: Optional[ComponentCondition] = Field(
        default=None,
        description="Current assessed condition of the component",
        example="repairable"
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
        description="Required approval signatures with name, ID, and timestamp",
        example={
            "inspector": {
                "name": "John Smith",
                "id": "INSP-001",
                "date": "2024-02-03T10:00:00"
            },
            "supervisor": {
                "name": "Jane Doe",
                "id": "SUP-001",
                "date": "2024-02-03T11:00:00"
            }
        }
    )
    certification: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Certification details including certificate number and documentation",
        example={
            "certificateNumber": "CERT-2024-001",
            "issueDate": "2024-02-03T12:00:00",
            "documentUrl": "https://nmis.scot/certificates/REP-2024-001.pdf"
        }
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
    defectManagement: Optional[str] = Field(
        default=None,
        description="Defect management workflow document, e.g., BPMN. URL to documentation."
    )
    remanufactureCostModel: Optional[str] = Field(
        default=None,
        description="ReManufacturing Cost Model - excel file. Filename or path."
    )
    remanufactureDESModel: Optional[str] = Field(
        default=None,
        description="High level parameterised opensource remanufacturing DES model. File or URL."
    )
    remanufactureSkills: Optional[str] = Field(
        default=None,
        description="Skills matrix of workforce needed to remanufacture. File or URL."
    )
    remanufactureEquipment: Optional[str] = Field(
        default=None,
        description="Required equipment to achieve successful remanufacturing. File or URL."
    )
    remanufactureCertification: Optional[str] = Field(
        default=None,
        description="Certification or Warranty documents for remanufactured product. File or URL."
    )
    remanufactureRepairId: Optional[str] = Field(
        default=None,
        description="Repair identifier. E.g., REP-2024-001"
    )