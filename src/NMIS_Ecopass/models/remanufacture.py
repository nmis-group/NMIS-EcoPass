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
                "componentInfo": {
                    "type": "turbineBlade",
                    "position": "stage1",
                    "operatingHours": 25000
                },
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
                        "testType": "dimensional",
                        "parameters": {"accuracy": 0.01},
                        "results": {"tipLength": 150.05, "tipWidth": 45.02},
                        "conformity": True,
                        "date": "2024-02-02T10:00:00",
                        "personnel": "INSP-TECH-002"
                    }
                ]
            }
        }
    )

    repairId: str = Field(
        description="Unique repair identifier"
    )
    componentInfo: Dict[str, Any] = Field(
        description="Component information including type, serial number, etc."
    )
    currentCondition: ComponentCondition = Field(
        description="Current condition assessment"
    )
    defects: Optional[Union[DefectInformation, List[DefectInformation]]] = Field(
        default=None,
        description="Identified defects"
    )
    repairHistory: Optional[Union[RepairHistory, List[RepairHistory]]] = Field(
        default=None,
        description="History of previous repairs"
    )
    processSteps: Optional[Union[ProcessStep, List[ProcessStep]]] = Field(
        default=None,
        description="Repair process steps"
    )
    testResults: Optional[Union[TestResult, List[TestResult]]] = Field(
        default=None,
        description="Test and inspection results"
    )
    qualityPlan: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Quality control requirements"
    )
    approvals: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Required approval signatures"
    )
    certification: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Certification information"
    )
    nextMaintenanceDue: Optional[datetime] = Field(
        default=None,
        description="Next maintenance due date"
    )
    restrictions: Optional[List[str]] = Field(
        default=None,
        description="Post-repair operational restrictions"
    )