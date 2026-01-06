"""Tests for BatteryPass models integration."""
import pytest
from pydantic import AnyUrl


def test_battery_pass_imports():
    """Test that all BatteryPass models can be imported."""
    from NMIS_Ecopass.models.BatteryPass import (
        BatteryPassport,
        GeneralProductInformation,
        CarbonFootprint,
        Circularity,
        MaterialComposition,
        PerformanceAndDurability,
        Labeling,
        SupplyChainDueDiligence,
        BatteryCategoryEnum,
        LifecycleStage,
    )
    
    # Verify these are proper Pydantic models
    assert hasattr(BatteryPassport, 'model_fields')
    assert hasattr(GeneralProductInformation, 'model_fields')
    assert hasattr(CarbonFootprint, 'model_fields')


def test_battery_pass_registry_integration():
    """Test that BatteryPassport is registered in SchemaRegistry."""
    from NMIS_Ecopass.models.registry import SchemaRegistry
    
    schemas = SchemaRegistry.list_all()
    assert 'battery_passport' in schemas
    assert 'battery_pass' in schemas
    
    # Can retrieve the schema
    bp_schema = SchemaRegistry.get_schema('battery_passport')
    assert bp_schema.__name__ == 'BatteryPassport'


def test_battery_category_enum():
    """Test BatteryCategoryEnum values match specification."""
    from NMIS_Ecopass.models.BatteryPass import BatteryCategoryEnum
    
    expected_categories = ['lmt', 'ev', 'industrial', 'stationary']
    actual_categories = [e.value for e in BatteryCategoryEnum]
    
    for cat in expected_categories:
        assert cat in actual_categories


def test_lifecycle_stage_enum():
    """Test LifecycleStage enum values match specification."""
    from NMIS_Ecopass.models.BatteryPass import LifecycleStage
    
    expected_stages = ['RawMaterialExtraction', 'MainProduction', 'Distribution', 'Recycling']
    actual_stages = [e.value for e in LifecycleStage]
    
    for stage in expected_stages:
        assert stage in actual_stages


def test_general_product_information_schema():
    """Test GeneralProductInformation model has expected fields."""
    from NMIS_Ecopass.models.BatteryPass import GeneralProductInformation
    
    fields = list(GeneralProductInformation.model_fields.keys())
    
    # Check key required fields per DIN DKE SPEC 99100
    assert 'productIdentifier' in fields
    assert 'batteryPassportIdentifier' in fields
    assert 'batteryCategory' in fields
    assert 'manufacturerInformation' in fields
    assert 'manufacturingDate' in fields
    assert 'batteryStatus' in fields
    assert 'batteryMass' in fields


def test_carbon_footprint_schema():
    """Test CarbonFootprint model has expected fields."""
    from NMIS_Ecopass.models.BatteryPass import CarbonFootprint
    
    fields = list(CarbonFootprint.model_fields.keys())
    
    assert 'batteryCarbonFootprint' in fields
    assert 'carbonFootprintPerLifecycleStage' in fields
    assert 'carbonFootprintPerformanceClass' in fields
    assert 'carbonFootprintStudy' in fields


def test_battery_passport_combined_model():
    """Test BatteryPassport combined model has all component fields."""
    from NMIS_Ecopass.models.BatteryPass import BatteryPassport
    
    fields = list(BatteryPassport.model_fields.keys())
    
    # Required components
    assert 'generalProductInformation' in fields
    assert 'carbonFootprint' in fields
    assert 'circularity' in fields
    assert 'materialComposition' in fields
    
    # Optional components
    assert 'performanceAndDurability' in fields
    assert 'labeling' in fields
    assert 'supplyChainDueDiligence' in fields
