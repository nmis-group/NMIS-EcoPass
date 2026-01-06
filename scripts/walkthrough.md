BatteryPass DPP Model Integration Walkthrough
Summary
Successfully integrated the BatteryPass Data Model v1.2.0 from the official GitHub repository into the NMIS_EcoPass package. Created reusable automation scripts for future DPP model imports.

What Was Done
1. Module Structure Created
src/NMIS_Ecopass/models/BatteryPass/
├── __init__.py                         # Module exports
├── battery_passport.py                 # Combined model
├── schemas/                            # Downloaded JSON schemas
│   ├── GeneralProductInformation-schema.json
│   ├── CarbonFootprintForBatteries-schema.json
│   ├── Circularity-schema.json
│   ├── MaterialComposition-schema.json
│   ├── PerformanceAndDurability-schema.json
│   ├── Labeling-schema.json
│   └── SupplyChainDueDiligence-schema.json
├── contexts/                           # JSON-LD contexts
│   └── *-ld.json files
├── general_product_information.py      # Generated Pydantic model
├── carbon_footprint.py
├── circularity.py
├── material_composition.py
├── performance_and_durability.py
├── labeling.py
└── supply_chain_due_diligence.py
2. Files Modified
File	Change
models/
init
.py
Added BatteryPass exports
models/registry.py
Added BatteryPassport auto-registration
pyproject.toml
Added datamodel-code-generator dev dependency
3. New Files Created
File	Purpose
BatteryPass/battery_passport.py
Combined passport model
tests/test_battery_pass.py
Unit tests for BatteryPass models
scripts/import_dpp_models.py
Automation script for future imports
Challenges & Solutions
UTF-16 LE Encoding Issue
WARNING

BatteryPass JSON schemas on GitHub are encoded as UTF-16 LE with BOM (\xff\xfe), not UTF-8.

Symptom: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0

Solution: Detect and handle encoding automatically:

if data.startswith(b'\xff\xfe'):
    content = data.decode('utf-16-le')
elif data.startswith(b'\xfe\xff'):
    content = data.decode('utf-16-be')
else:
    content = data.decode('utf-8')
Generated Models Named "Model"
datamodel-code-generator names the root class 
Model
. We renamed in exports:

from .general_product_information import Model as GeneralProductInformation
Usage
Import BatteryPassport in Code
from NMIS_Ecopass.models import BatteryPassport
from NMIS_Ecopass.models.BatteryPass import (
    GeneralProductInformation,
    CarbonFootprint,
    BatteryCategoryEnum,
    LifecycleStage
)
# Use via SchemaRegistry
from NMIS_Ecopass.models.registry import SchemaRegistry
schema = SchemaRegistry.get_schema('battery_passport')
Importing New DPP Models (Future)
Use the automation script:

poetry run python scripts/import_dpp_models.py \
    --repo "owner/RepoName" \
    --model-name "ModelName" \
    --branch "main"
Or use the workflow: /import-dpp-models

Verification
# Run tests
poetry run pytest tests/test_battery_pass.py -v
# Verify imports
poetry run python -c "from NMIS_Ecopass.models import BatteryPassport; print(list(BatteryPassport.model_fields.keys()))"