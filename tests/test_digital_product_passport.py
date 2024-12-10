import pytest
from datetime import datetime
from uuid import UUID
from pydantic import ValidationError

from NMIS_Ecopass.models.digitalProductPassport import DigitalProductPassport
from NMIS_Ecopass.models.metadata import Metadata, StatusEnum
from NMIS_Ecopass.models.productIdentifier import ProductIdentifier, ProductStatus
from NMIS_Ecopass.models.circularity import (
    Circularity, DocumentType, MimeType, ResourcePath
)
from NMIS_Ecopass.models.carbonFootprint import (
    CarbonFootprint, LifecycleStage, LifecycleStageCarbonFootprint
)
from NMIS_Ecopass.models.remanufacture import (
    RepairModel, ProcessCategory, RepairType, ComponentCondition
)
from NMIS_Ecopass.models.materialComposition import (
    MaterialInformation, MaterialCategory, MaterialForm, MaterialStandard
)

def test_create_minimal_passport():
    """Test creating a minimal digital product passport"""
    passport = DigitalProductPassport()
    assert isinstance(passport.metadata, Metadata)
    assert isinstance(passport.productIdentifier, ProductIdentifier)
    assert isinstance(passport.circularity, Circularity)
    assert isinstance(passport.carbonFootprint, CarbonFootprint)
    assert isinstance(passport.reManufacture, RepairModel)
    assert isinstance(passport.materialInformation, MaterialInformation)

def test_create_complete_passport():
    """Test creating a complete digital product passport with all fields"""
    passport = DigitalProductPassport(
        metadata=Metadata(
            economic_operator_id="ECO-123456789",
            issue_date=datetime.now(),
            status=StatusEnum.ACTIVE
        ),
        productIdentifier=ProductIdentifier(
            batchID="BCH-20240913-001",
            serialID="SN-AB123456789",
            productStatus=ProductStatus.ORIGINAL
        ),
        circularity=Circularity(
            dismantlingAndRemovalInformation=[{
                "documentType": DocumentType.DISMANTLINGMANUAL,
                "mimeType": MimeType.PDF,
                "documentURL": ResourcePath(
                    resourcePath="https://example.com/manual.pdf"
                )
            }]
        ),
        carbonFootprint=CarbonFootprint(
            carbonFootprintPerLifecycleStage=[
                LifecycleStageCarbonFootprint(
                    lifecycleStage=LifecycleStage.RAWMATERIALEXTRACTION,
                    carbonFootprint=20.5
                )
            ],
            productCarbonFootprint=100.0
        ),
        reManufacture=RepairModel(
            repairId="REP-2024-001",
            componentInfo={"type": "turbineBlade"},
            currentCondition=ComponentCondition.SERVICEABLE
        ),
        materialInformation=MaterialInformation(
            materialId="MAT-2024-001",
            tradeName="Inconel 718",
            materialCategory=MaterialCategory.METAL,
            materialStandard=MaterialStandard.ASTM,
            standardDesignation="ASTM B637",
            composition=[],
            materialForm=MaterialForm.BAR,
            properties=[],
            traceability={
                "batchNumber": "BATCH-001",
                "manufacturer": "ACME Corp",
                "productionDate": datetime.now()
            }
        )
    )
    
    assert passport.metadata.economic_operator_id == "ECO-123456789"
    assert passport.productIdentifier.serialID == "SN-AB123456789"
    assert passport.carbonFootprint.productCarbonFootprint == 100.0
    assert passport.materialInformation.tradeName == "Inconel 718"

def test_passport_validation():
    """Test validation of digital product passport data"""
    with pytest.raises(ValidationError):
        DigitalProductPassport(
            productIdentifier=ProductIdentifier(
                batchID="123",  # Valid
                serialID="123",  # Valid
                productStatus="invalid"  # Invalid status
            )
        )

def test_passport_serialization():
    """Test serialization of digital product passport"""
    passport = DigitalProductPassport(
        metadata=Metadata(
            economic_operator_id="ECO-123456789",
            issue_date=datetime.now(),
            status=StatusEnum.ACTIVE
        )
    )
    
    passport_dict = passport.model_dump()
    assert isinstance(passport_dict, dict)
    assert "metadata" in passport_dict
    assert passport_dict["metadata"]["economic_operator_id"] == "ECO-123456789"

def test_passport_update():
    """Test updating passport fields"""
    passport = DigitalProductPassport()
    
    # Update product identifier
    passport.productIdentifier.productStatus = ProductStatus.REPAIRED
    assert passport.productIdentifier.productStatus == ProductStatus.REPAIRED
    
    # Update carbon footprint
    passport.carbonFootprint.productCarbonFootprint = 150.0
    assert passport.carbonFootprint.productCarbonFootprint == 150.0

def test_nested_validation():
    """Test validation of nested models"""
    with pytest.raises(ValidationError):
        DigitalProductPassport(
            materialInformation=MaterialInformation(
                materialId="MAT-2024-001",
                tradeName="Inconel 718",
                materialCategory="invalid_category",  # Invalid category
                materialStandard=MaterialStandard.ASTM,
                standardDesignation="ASTM B637",
                composition=[],
                materialForm=MaterialForm.BAR,
                properties=[],
                traceability={
                    "batchNumber": "BATCH-001",
                    "manufacturer": "ACME Corp",
                    "productionDate": datetime.now()
                }
            )
        )