"""
BatteryPass Data Model v1.2.0

Pydantic models auto-generated from the official BatteryPass JSON schemas.
Reference: https://github.com/batterypass/BatteryPassDataModel

This module provides type-safe models for the EU Battery Regulation
Digital Product Passport requirements.
"""

# Combined passport model
from .battery_passport import BatteryPassport

# Individual component models (renamed from "Model" for clarity)
from .general_product_information import Model as GeneralProductInformation
from .carbon_footprint import Model as CarbonFootprint
from .circularity import Model as Circularity
from .material_composition import Model as MaterialComposition
from .performance_and_durability import Model as PerformanceAndDurability
from .labeling import Model as Labeling
from .supply_chain_due_diligence import Model as SupplyChainDueDiligence

# Re-export commonly used enums
from .general_product_information import (
    BatteryCategoryEnum,
    BatteryStatusEnumeration,
)
from .carbon_footprint import LifecycleStage
from .circularity import Documenttype, RecycledMaterial
from .material_composition import HazardousSubstanceClassChrateristicEnum
from .labeling import LabelingSubject

__all__ = [
    # Main passport model
    "BatteryPassport",
    # Component models
    "GeneralProductInformation",
    "CarbonFootprint", 
    "Circularity",
    "MaterialComposition",
    "PerformanceAndDurability",
    "Labeling",
    "SupplyChainDueDiligence",
    # Commonly used enums
    "BatteryCategoryEnum",
    "BatteryStatusEnumeration",
    "LifecycleStage",
    "Documenttype",
    "RecycledMaterial",
    "HazardousSubstanceClassChrateristicEnum",
    "LabelingSubject",
]
