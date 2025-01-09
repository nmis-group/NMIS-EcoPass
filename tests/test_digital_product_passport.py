import pytest
from datetime import datetime
from pydantic import ValidationError

from NMIS_Ecopass.models.digitalProductPassport import DigitalProductPassport
from NMIS_Ecopass.models.metadata import Metadata, StatusEnum
from NMIS_Ecopass.models.productIdentifier import ProductIdentifier, ProductStatus
from NMIS_Ecopass.models.remanufacture import RepairModel, ComponentCondition

def test_create_minimal_passport():
    """Test creating a minimal digital product passport"""
    passport = DigitalProductPassport(
        reManufacture=RepairModel(
            repairId="REP-001",
            componentInfo={"type": "generic"},
            currentCondition=ComponentCondition.UNKNOWN
        ),
        productMaterial={
            "productId": "PROD-001",
            "components": {
                "main": {
                    "materialId": "MAT-001",
                    "tradeName": "Generic Material",
                    "materialCategory": "other",
                    "materialStandard": "custom",
                    "standardDesignation": "N/A",
                    "composition": [{
                        "element": "Generic",
                        "unit": "weight_percent"
                    }],
                    "materialForm": "solid",
                    "properties": [{
                        "propertyName": "density",
                        "value": 1.0,
                        "unit": "g/cm3"
                    }],
                    "traceability": {
                        "batchNumber": "BATCH-001"
                    }
                }
            },
            "totalMass": 1.0,
            "materialBreakdown": {"generic": 100.0}
        }
    )
    
    # Test that required fields are created with default values
    assert isinstance(passport.metadata, Metadata)
    assert isinstance(passport.productIdentifier, ProductIdentifier)
    assert isinstance(passport.reManufacture, RepairModel)
    assert passport.productMaterial.productId == "PROD-001"

def test_create_complete_passport():
    """Test creating a complete digital product passport"""
    passport = DigitalProductPassport(
        metadata=Metadata(
            economic_operator_id="ECO-001",
            issue_date=datetime.now(),
            status=StatusEnum.ACTIVE
        ),
        productIdentifier=ProductIdentifier(
            batchID="BATCH-001",
            serialID="SN-001",
            productStatus=ProductStatus.ORIGINAL
        ),
        reManufacture=RepairModel(
            repairId="REP-001",
            componentInfo={"type": "generic"},
            currentCondition=ComponentCondition.SERVICEABLE
        ),
        productMaterial={
            "productId": "PROD-001",
            "components": {
                "main": {
                    "materialId": "MAT-001",
                    "tradeName": "Test Material",
                    "materialCategory": "metal",
                    "materialStandard": "astm",
                    "standardDesignation": "ASTM-001",
                    "composition": [{
                        "element": "Fe",
                        "unit": "weight_percent"
                    }],
                    "materialForm": "bar",
                    "properties": [{
                        "propertyName": "density",
                        "value": 7.8,
                        "unit": "g/cm3"
                    }],
                    "traceability": {
                        "batchNumber": "BATCH-001"
                    }
                }
            },
            "totalMass": 1.0,
            "materialBreakdown": {"metal": 100.0}
        }
    )
    
    # Test that fields are set correctly
    assert passport.metadata.economic_operator_id == "ECO-001"
    assert passport.productIdentifier.serialID == "SN-001"
    assert passport.reManufacture.repairId == "REP-001"
    assert passport.productMaterial.productId == "PROD-001"

def test_passport_validation():
    """Test validation of digital product passport"""
    with pytest.raises(ValidationError):
        DigitalProductPassport(
            productIdentifier=ProductIdentifier(
                batchID="123",
                serialID="123",
                productStatus="invalid_status"  # Invalid status
            )
        )

def test_passport_serialization():
    """Test serialization of digital product passport"""
    passport = DigitalProductPassport(
        reManufacture=RepairModel(
            repairId="REP-001",
            componentInfo={"type": "generic"},
            currentCondition=ComponentCondition.UNKNOWN
        ),
        productMaterial={
            "productId": "PROD-001",
            "components": {
                "main": {
                    "materialId": "MAT-001",
                    "tradeName": "Generic Material",
                    "materialCategory": "other",
                    "materialStandard": "custom",
                    "standardDesignation": "N/A",
                    "composition": [{
                        "element": "Generic",
                        "unit": "weight_percent"
                    }],
                    "materialForm": "solid",
                    "properties": [{
                        "propertyName": "density",
                        "value": 1.0,
                        "unit": "g/cm3"
                    }],
                    "traceability": {
                        "batchNumber": "BATCH-001"
                    }
                }
            },
            "totalMass": 1.0,
            "materialBreakdown": {"generic": 100.0}
        }
    )
    
    # Test serialization to dict
    passport_dict = passport.model_dump()
    assert isinstance(passport_dict, dict)
    assert "metadata" in passport_dict
    assert "productIdentifier" in passport_dict
    assert "reManufacture" in passport_dict
    assert "productMaterial" in passport_dict