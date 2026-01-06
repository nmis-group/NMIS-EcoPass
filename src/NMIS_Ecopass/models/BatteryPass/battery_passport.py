"""
BatteryPass Data Model v1.2.0

Combined Battery Passport model that composes all 7 component categories
from the official BatteryPass specification.

Reference: https://github.com/batterypass/BatteryPassDataModel
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

# Import root models from each component (they're named "Model" in generated files)
from .general_product_information import Model as GeneralProductInformation
from .carbon_footprint import Model as CarbonFootprint
from .circularity import Model as Circularity
from .material_composition import Model as MaterialComposition
from .performance_and_durability import Model as PerformanceAndDurability
from .labeling import Model as Labeling
from .supply_chain_due_diligence import Model as SupplyChainDueDiligence


class BatteryPassport(BaseModel):
    """
    Complete Battery Passport Data Model v1.2.0.
    
    Combines all 7 component categories as specified by the Battery Pass Project
    and DIN DKE SPEC 99100:2025-02.
    
    Components:
    - General Product Information (required)
    - Carbon Footprint (required)
    - Circularity (required)
    - Material Composition (required)
    - Performance & Durability (optional)
    - Labels & Certification (optional)
    - Supply Chain Due Diligence (optional)
    """
    
    generalProductInformation: GeneralProductInformation = Field(
        ...,
        description="General product and manufacturer information including battery ID, status, and warranty"
    )
    
    carbonFootprint: CarbonFootprint = Field(
        ...,
        description="Carbon footprint data including per-lifecycle-stage breakdown and performance class"
    )
    
    circularity: Circularity = Field(
        ...,
        description="Circularity information including recycled content, dismantling info, and end-of-life handling"
    )
    
    materialComposition: MaterialComposition = Field(
        ...,
        description="Material composition data including battery chemistry, materials, and hazardous substances"
    )
    
    performanceAndDurability: Optional[PerformanceAndDurability] = Field(
        default=None,
        description="Performance and durability metrics including capacity, power, SoH, and negative events"
    )
    
    labeling: Optional[Labeling] = Field(
        default=None,
        description="Labels and certification including declaration of conformity and test reports"
    )
    
    supplyChainDueDiligence: Optional[SupplyChainDueDiligence] = Field(
        default=None,
        description="Supply chain due diligence report and third-party assurances"
    )
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"
        json_schema_extra = {
            "title": "Battery Passport",
            "description": "Battery Passport Data Model v1.2.0 per DIN DKE SPEC 99100"
        }
