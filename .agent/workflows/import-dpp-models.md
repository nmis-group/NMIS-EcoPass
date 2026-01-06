---
description: Import DPP models from external GitHub repositories containing JSON schemas
---

# Import External DPP Data Models

This workflow automates the process of integrating Digital Product Passport (DPP) data models from external GitHub repositories into the NMIS_Ecopass package.

## Prerequisites
- `datamodel-code-generator` installed (dev dependency): `poetry add --group dev datamodel-code-generator`
- Python 3.10+

## Workflow Steps

### 1. Identify the Schema Repository
Find the GitHub repository containing JSON schemas. Common patterns:
- Look for `*-schema.json` files in `/gen/` folders
- Look for `*-ld.json` files for JSON-LD contexts
- Check for RDF/Turtle (`.ttl`) source files

Example repositories:
- BatteryPass: `https://github.com/batterypass/BatteryPassDataModel`
- TextilePass: (when available)

### 2. Run the Import Script
```bash
# From project root
poetry run python scripts/import_dpp_models.py \
    --repo-url "https://github.com/batterypass/BatteryPassDataModel" \
    --model-name "BatteryPass" \
    --schema-path "BatteryPass/*/gen/*-schema.json"
```

### 3. Verify Generated Models
// turbo
```bash
poetry run pytest tests/test_<model_name>.py -v
```

### 4. Register in SchemaRegistry
The script auto-registers, but verify:
```python
from NMIS_Ecopass.models.registry import SchemaRegistry
print(SchemaRegistry.list_all())  # Should include new model
```

## Manual Process (Reference)

If the script fails, follow these manual steps:

### Step 1: Create Module Structure
```bash
mkdir -p src/NMIS_Ecopass/models/<ModelName>/schemas
mkdir -p src/NMIS_Ecopass/models/<ModelName>/contexts
```

### Step 2: Download JSON Schemas
⚠️ **Important**: GitHub files may be UTF-16 LE encoded. Use Python with encoding detection:

```python
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://raw.githubusercontent.com/..."
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as r:
    data = r.read()
    # Detect UTF-16 LE BOM
    if data.startswith(b'\xff\xfe'):
        content = data.decode('utf-16-le')
    else:
        content = data.decode('utf-8')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
```

### Step 3: Generate Pydantic Models
```bash
poetry run datamodel-codegen \
    --input "src/NMIS_Ecopass/models/<ModelName>/schemas/<schema>.json" \
    --output "src/NMIS_Ecopass/models/<ModelName>/<module>.py" \
    --output-model-type pydantic_v2.BaseModel \
    --use-annotated \
    --use-field-description \
    --collapse-root-models
```

### Step 4: Create Combined Model
Create `<model_name>_passport.py` that imports and combines all component models.

### Step 5: Create `__init__.py`
Export all models and commonly used enums.

### Step 6: Update Registry
Add auto-registration in `models/registry.py`.

### Step 7: Update Package Exports
Add import in `models/__init__.py`.

## Troubleshooting

### Unicode Decode Error
GitHub raw files may be UTF-16. Use the encoding detection shown above.

### Missing $ref Definitions
Some schemas have external references. You may need to:
1. Download all referenced schemas first
2. Use `--base-class` flag if needed

### Model Named "Model"
Generated code uses `Model` as class name. Rename in `__init__.py`:
```python
from .component import Model as ComponentName
```
