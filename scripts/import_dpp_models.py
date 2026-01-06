#!/usr/bin/env python
"""
Import DPP Models from External GitHub Repositories

This script automates the process of:
1. Discovering JSON schemas in a GitHub repository
2. Downloading them with proper encoding handling
3. Generating Pydantic v2 models using datamodel-code-generator
4. Creating module structure and exports
5. Registering in SchemaRegistry

Usage:
    python scripts/import_dpp_models.py --help
    python scripts/import_dpp_models.py \
        --repo "batterypass/BatteryPassDataModel" \
        --model-name "BatteryPass" \
        --branch "main" \
        --schema-pattern "BatteryPass/*/gen/*-schema.json"

Example for BatteryPass:
    python scripts/import_dpp_models.py \
        --repo "batterypass/BatteryPassDataModel" \
        --model-name "BatteryPass"
"""
import argparse
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple


# SSL context for corporate proxies
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def fetch_url(url: str) -> bytes:
    """Fetch content from URL with proper headers."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as response:
        return response.read()


def decode_content(data: bytes) -> str:
    """Decode content handling various encodings (UTF-16 LE BOM, UTF-8, etc.)."""
    # Check for UTF-16 LE BOM
    if data.startswith(b'\xff\xfe'):
        return data.decode('utf-16-le')
    # Check for UTF-16 BE BOM
    elif data.startswith(b'\xfe\xff'):
        return data.decode('utf-16-be')
    # Check for UTF-8 BOM
    elif data.startswith(b'\xef\xbb\xbf'):
        return data[3:].decode('utf-8')
    # Default to UTF-8
    else:
        return data.decode('utf-8')


def find_schemas_in_repo(repo: str, branch: str = "main") -> List[Tuple[str, str]]:
    """
    Find all JSON schema files in a GitHub repository.
    
    Returns list of (filename, raw_url) tuples.
    """
    # Use GitHub API to list repository contents
    api_url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    
    try:
        data = fetch_url(api_url)
        tree = json.loads(decode_content(data))
    except Exception as e:
        print(f"Warning: Could not fetch repo tree via API: {e}")
        print("Trying known BatteryPass schema paths...")
        return get_batterypass_schemas(repo, branch)
    
    schemas = []
    for item in tree.get('tree', []):
        path = item.get('path', '')
        if path.endswith('-schema.json') and '/gen/' in path:
            filename = os.path.basename(path)
            raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
            schemas.append((filename, raw_url))
    
    return schemas


def get_batterypass_schemas(repo: str, branch: str = "main") -> List[Tuple[str, str]]:
    """Known BatteryPass schema paths for fallback."""
    base = f"https://raw.githubusercontent.com/{repo}/{branch}/BatteryPass"
    
    schemas = [
        ('GeneralProductInformation-schema.json', 
         f'{base}/io.BatteryPass.GeneralProductInformation/1.2.0/gen/GeneralProductInformation-schema.json'),
        ('CarbonFootprintForBatteries-schema.json',
         f'{base}/io.BatteryPass.CarbonFootprint/1.2.0/gen/CarbonFootprintForBatteries-schema.json'),
        ('Circularity-schema.json',
         f'{base}/io.BatteryPass.Circularity/1.2.0/gen/Circularity-schema.json'),
        ('MaterialComposition-schema.json',
         f'{base}/io.BatteryPass.MaterialComposition/1.2.0/gen/MaterialComposition-schema.json'),
        ('PerformanceAndDurability-schema.json',
         f'{base}/io.BatteryPass.Performance/1.2.0/gen/PerformanceAndDurability-schema.json'),
        ('Labeling-schema.json',
         f'{base}/io.BatteryPass.Labels/1.2.0/gen/Labeling-schema.json'),
        ('SupplyChainDueDiligence-schema.json',
         f'{base}/io.BatteryPass.SupplyChainDueDiligence/1.2.0/gen/SupplyChainDueDiligence-schema.json'),
    ]
    return schemas


def find_contexts_in_repo(repo: str, branch: str = "main") -> List[Tuple[str, str]]:
    """Find JSON-LD context files in repository."""
    api_url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    
    try:
        data = fetch_url(api_url)
        tree = json.loads(decode_content(data))
    except Exception:
        return get_batterypass_contexts(repo, branch)
    
    contexts = []
    for item in tree.get('tree', []):
        path = item.get('path', '')
        if path.endswith('-ld.json') and '/gen/' in path:
            filename = os.path.basename(path)
            raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
            contexts.append((filename, raw_url))
    
    return contexts


def get_batterypass_contexts(repo: str, branch: str = "main") -> List[Tuple[str, str]]:
    """Known BatteryPass JSON-LD context paths for fallback."""
    base = f"https://raw.githubusercontent.com/{repo}/{branch}/BatteryPass"
    
    contexts = [
        ('GeneralProductInformation-ld.json',
         f'{base}/io.BatteryPass.GeneralProductInformation/1.2.0/gen/GeneralProductInformation-ld.json'),
        ('CarbonFootprintForBatteries-ld.json',
         f'{base}/io.BatteryPass.CarbonFootprint/1.2.0/gen/CarbonFootprintForBatteries-ld.json'),
        ('Circularity-ld.json',
         f'{base}/io.BatteryPass.Circularity/1.2.0/gen/Circularity-ld.json'),
        ('MaterialComposition-ld.json',
         f'{base}/io.BatteryPass.MaterialComposition/1.2.0/gen/MaterialComposition-ld.json'),
        ('PerformanceAndDurability-ld.json',
         f'{base}/io.BatteryPass.Performance/1.2.0/gen/PerformanceAndDurability-ld.json'),
        ('Labeling-ld.json',
         f'{base}/io.BatteryPass.Labels/1.2.0/gen/Labeling-ld.json'),
        ('SupplyChainDueDiligence-ld.json',
         f'{base}/io.BatteryPass.SupplyChainDueDiligence/1.2.0/gen/SupplyChainDueDiligence-ld.json'),
    ]
    return contexts


def download_file(url: str, dest_path: Path) -> bool:
    """Download a file with encoding handling."""
    try:
        print(f"  Downloading {dest_path.name}...")
        data = fetch_url(url)
        content = decode_content(data)
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"    Error: {e}")
        return False


def schema_to_module_name(schema_filename: str) -> str:
    """Convert schema filename to Python module name."""
    # Remove -schema.json suffix
    name = schema_filename.replace('-schema.json', '')
    # Convert CamelCase to snake_case
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    # Handle "ForBatteries" suffix
    name = name.replace('_for_batteries', '')
    return name


def generate_pydantic_model(schema_path: Path, output_path: Path) -> bool:
    """Generate Pydantic model from JSON schema using datamodel-codegen."""
    cmd = [
        sys.executable, '-m', 'datamodel_code_generator',
        '--input', str(schema_path),
        '--output', str(output_path),
        '--output-model-type', 'pydantic_v2.BaseModel',
        '--use-annotated',
        '--use-field-description',
        '--collapse-root-models',
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"    Error running datamodel-codegen: {e}")
        return False


def create_combined_model(model_name: str, modules: List[str], output_path: Path):
    """Create a combined passport model that composes all components."""
    imports = []
    fields = []
    
    for module in modules:
        class_name = ''.join(word.title() for word in module.split('_'))
        imports.append(f"from .{module} import Model as {class_name}")
        
        # Determine if field is required or optional
        is_optional = module in ['performance_and_durability', 'labeling', 'supply_chain_due_diligence']
        
        if is_optional:
            fields.append(f'''    {module}: Optional[{class_name}] = Field(
        default=None,
        description="{class_name} component"
    )''')
        else:
            fields.append(f'''    {module}: {class_name} = Field(
        ...,
        description="{class_name} component"
    )''')
    
    content = f'''"""
{model_name} Combined Passport Model

Auto-generated combined model composing all component categories.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

{chr(10).join(imports)}


class {model_name}Passport(BaseModel):
    """
    Combined {model_name} Passport Data Model.
    
    Composes all component categories from the official specification.
    """
    
{chr(10).join(fields)}
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"
        json_schema_extra = {{
            "title": "{model_name} Passport",
            "description": "{model_name} Digital Product Passport"
        }}
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def create_init_file(model_name: str, modules: List[str], output_path: Path):
    """Create __init__.py with proper exports."""
    imports = [f"from .{model_name.lower()}_passport import {model_name}Passport"]
    all_exports = [f'"{model_name}Passport"']
    
    for module in modules:
        class_name = ''.join(word.title() for word in module.split('_'))
        imports.append(f"from .{module} import Model as {class_name}")
        all_exports.append(f'"{class_name}"')
    
    content = f'''"""
{model_name} Data Model

Pydantic models auto-generated from official JSON schemas.
"""

{chr(10).join(imports)}

__all__ = [
    {("," + chr(10) + "    ").join(all_exports)},
]
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def update_registry(model_name: str, registry_path: Path):
    """Add model registration to registry.py."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already registered
    if f"'{model_name.lower()}_passport'" in content.lower():
        print(f"  {model_name} already registered in SchemaRegistry")
        return
    
    # Find the _auto_register_schemas function and add registration
    registration_code = f'''
    try:
        from ..models.{model_name} import {model_name}Passport
        SchemaRegistry.register('{model_name.lower()}_passport', {model_name}Passport)
        SchemaRegistry.register('{model_name.lower().replace("pass", "_pass")}', {model_name}Passport)
    except ImportError:
        pass
'''
    
    # Insert before "# Auto-register on import"
    marker = "# Auto-register on import"
    if marker in content:
        content = content.replace(marker, registration_code + "\n" + marker)
        with open(registry_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Registered {model_name}Passport in SchemaRegistry")


def update_models_init(model_name: str, init_path: Path):
    """Add model import to models/__init__.py."""
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import_line = f"from .{model_name} import *"
    if import_line not in content:
        content = content.rstrip() + f"\n{import_line}\n"
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Added {model_name} to models/__init__.py")


def main():
    parser = argparse.ArgumentParser(
        description="Import DPP models from external GitHub repositories"
    )
    parser.add_argument(
        '--repo', '-r',
        required=True,
        help='GitHub repository (e.g., "batterypass/BatteryPassDataModel")'
    )
    parser.add_argument(
        '--model-name', '-n',
        required=True,
        help='Name for the model module (e.g., "BatteryPass")'
    )
    parser.add_argument(
        '--branch', '-b',
        default='main',
        help='Git branch (default: main)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='src/NMIS_Ecopass/models',
        help='Output directory for models'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    # Paths
    base_path = Path(args.output_dir) / args.model_name
    schemas_path = base_path / 'schemas'
    contexts_path = base_path / 'contexts'
    registry_path = Path(args.output_dir) / 'registry.py'
    models_init_path = Path(args.output_dir) / '__init__.py'
    
    print(f"\n{'='*60}")
    print(f"Importing DPP Models: {args.model_name}")
    print(f"Repository: {args.repo} (branch: {args.branch})")
    print(f"Output: {base_path}")
    print(f"{'='*60}\n")
    
    if args.dry_run:
        print("[DRY RUN - No changes will be made]\n")
    
    # Step 1: Find and download schemas
    print("Step 1: Finding JSON schemas...")
    schemas = find_schemas_in_repo(args.repo, args.branch)
    print(f"  Found {len(schemas)} schemas")
    
    if not args.dry_run:
        print("\nStep 2: Downloading schemas...")
        for filename, url in schemas:
            download_file(url, schemas_path / filename)
    
    # Step 3: Find and download JSON-LD contexts
    print("\nStep 3: Finding JSON-LD contexts...")
    contexts = find_contexts_in_repo(args.repo, args.branch)
    print(f"  Found {len(contexts)} contexts")
    
    if not args.dry_run:
        print("\nStep 4: Downloading contexts...")
        for filename, url in contexts:
            download_file(url, contexts_path / filename)
    
    # Step 5: Generate Pydantic models
    print("\nStep 5: Generating Pydantic models...")
    modules = []
    
    for filename, _ in schemas:
        module_name = schema_to_module_name(filename)
        modules.append(module_name)
        
        if args.dry_run:
            print(f"  Would generate: {module_name}.py")
        else:
            schema_file = schemas_path / filename
            output_file = base_path / f"{module_name}.py"
            print(f"  Generating {module_name}.py...")
            generate_pydantic_model(schema_file, output_file)
    
    # Step 6: Create combined model
    print(f"\nStep 6: Creating combined {args.model_name}Passport model...")
    if not args.dry_run:
        create_combined_model(
            args.model_name, 
            modules, 
            base_path / f"{args.model_name.lower()}_passport.py"
        )
    
    # Step 7: Create __init__.py
    print(f"\nStep 7: Creating __init__.py...")
    if not args.dry_run:
        create_init_file(args.model_name, modules, base_path / '__init__.py')
    
    # Step 8: Update registry
    print(f"\nStep 8: Updating SchemaRegistry...")
    if not args.dry_run and registry_path.exists():
        update_registry(args.model_name, registry_path)
    
    # Step 9: Update models/__init__.py
    print(f"\nStep 9: Updating models/__init__.py...")
    if not args.dry_run and models_init_path.exists():
        update_models_init(args.model_name, models_init_path)
    
    print(f"\n{'='*60}")
    print("Import complete!")
    print(f"{'='*60}")
    print(f"\nVerify with:")
    print(f"  poetry run python -c \"from NMIS_Ecopass.models.{args.model_name} import {args.model_name}Passport; print({args.model_name}Passport.model_fields.keys())\"")
    print(f"\nRun tests:")
    print(f"  poetry run pytest tests/ -v")


if __name__ == '__main__':
    main()
