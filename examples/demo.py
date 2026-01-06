"""
DPP Bridge Quick Demo

Run this script to test the prototype:
    python examples/demo.py
"""

from pathlib import Path
import json

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from NMIS_Ecopass import DPPBridge


def demo_isa95():
    """Demo: Transform ISA-95 XML to DPP."""
    print("=" * 50)
    print("Demo 1: ISA-95 XML → Battery DPP")
    print("=" * 50)
    
    examples_dir = Path(__file__).parent
    
    bridge = DPPBridge()
    
    results = bridge.transform(
        source=examples_dir / "battery_production.xml",
        mapping=examples_dir / "isa95_to_battery.yaml",
        output=examples_dir / "output_battery_dpp.json"
    )
    
    print(f"\nTransformed {len(results)} record(s)")
    print("\nFirst result:")
    print(json.dumps(results[0], indent=2))
    print(f"\nOutput saved to: {examples_dir / 'output_battery_dpp.json'}")


def demo_csv():
    """Demo: Transform CSV to DPP."""
    print("\n" + "=" * 50)
    print("Demo 2: CSV → Textile DPP")
    print("=" * 50)
    
    examples_dir = Path(__file__).parent
    
    bridge = DPPBridge()
    
    results = bridge.transform(
        source=examples_dir / "textile_products.csv",
        mapping=examples_dir / "csv_to_textile.yaml",
        output=examples_dir / "output_textile_dpp.json"
    )
    
    print(f"\nTransformed {len(results)} record(s)")
    print("\nFirst result:")
    print(json.dumps(results[0], indent=2))
    print(f"\nOutput saved to: {examples_dir / 'output_textile_dpp.json'}")


def demo_stepwise():
    """Demo: Step-by-step transformation."""
    print("\n" + "=" * 50)
    print("Demo 3: Step-by-step API")
    print("=" * 50)
    
    examples_dir = Path(__file__).parent
    
    bridge = DPPBridge()
    
    # Step 1: Extract
    print("\n1. Extracting data from CSV...")
    records = bridge.extract(
        examples_dir / "textile_products.csv",
        connector="csv"
    )
    print(f"   Extracted {len(records)} records")
    
    # Step 2: Map
    print("\n2. Applying transformations...")
    transformed = bridge.map(
        records,
        mapping=examples_dir / "csv_to_textile.yaml"
    )
    print(f"   Transformed {len(transformed)} records")
    
    # Step 3: Export
    print("\n3. Exporting to JSON-LD...")
    bridge.export(
        transformed,
        output=examples_dir / "output_stepwise.json",
        format="jsonld"
    )
    print(f"   Saved to: {examples_dir / 'output_stepwise.json'}")





def demo_batterypass_mapping_validation():
    """Demo: Auto-generate Battery Passport using YAML mapping and validate with Pydantic."""
    print("\n" + "=" * 50)
    print("Demo 4: YAML Mapping -> BatteryPass Validation")
    print("=" * 50)
    
    examples_dir = Path(__file__).parent
    bridge = DPPBridge()

    print("\n1. Transforming ISA-95 XML using 'isa95_to_battery.yaml'...")
    # Transform using the bridge (ETL)
    try:
        results = bridge.transform(
            source=examples_dir / "battery_production.xml",
            mapping=examples_dir / "isa95_to_battery.yaml",
            # We don't save to file here yet, just get the dicts
        )
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        return

    if not results:
        print("❌ No results generated.")
        return

    print(f"   Generated {len(results)} passport record(s).")
    
    # Helper to fix list generation (mapping engine produces {"0": ...} instead of lists)
    def clean_lists(obj):
        if isinstance(obj, dict):
            # Check if all keys are numeric strings
            if obj and all(k.isdigit() for k in obj.keys()):
                # Convert to list sorted by index
                return [clean_lists(obj[k]) for k in sorted(obj.keys(), key=int)]
            return {k: clean_lists(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_lists(x) for x in obj]
        return obj

    print("\n2. Validating against BatteryPass Pydantic Model...")
    try:
        from NMIS_Ecopass.models.BatteryPass import BatteryPassport
    except ImportError:
        print("❌ BatteryPass models not found.")
        return

    # Validate each result
    for i, record in enumerate(results):
        print(f"   Validating Record #{i+1}...")
        try:
            # Clean up the record (convert "0":... dicts to lists)
            cleaned_record = clean_lists(record)
            
            # The bridge output is a dict. We validate it against the model.
            passport = BatteryPassport.model_validate(cleaned_record)
            print(f"   ✅ Record #{i+1} is VALID!")
            
            # Print a snippet
            print(f"   Passport ID: {passport.generalProductInformation.batteryPassportIdentifier}")
            print(f"   Product ID: {passport.generalProductInformation.productIdentifier}")
            
        except Exception as e:
            print(f"   ❌ Record #{i+1} INVALID:")
            print(e)

    # Save the first validated one for inspection
    if results:
         with open(examples_dir / "output_battery_mapping.json", "w") as f:
             # Use the Pydantic model dump to ensure cleaner JSON
             try:
                 p = BatteryPassport.model_validate(results[0])
                 f.write(p.model_dump_json(indent=2, exclude_none=True))
                 print(f"\nSaved valid passport to: {examples_dir / 'output_battery_mapping.json'}")
             except:
                 import json
                 json.dump(results[0], f, indent=2)
                 print(f"\nSaved raw passport to: {examples_dir / 'output_battery_mapping.json'}")


def demo_api_mode():
    """
    Demo 5: API Mode - Direct JSON Validation for Automation Tools.
    
    This demo shows how companies can integrate DPP creation with automation
    tools like Microsoft Power Automate, Azure Logic Apps, or Zapier.
    
    Features demonstrated:
    - Direct JSON payload validation (no file I/O required)
    - JSON Schema export for OpenAPI/Swagger integration  
    - Compliance percentage tracking per section
    - Field requirements listing (required vs optional)
    - QR code generation for physical product labeling
    """
    print("\n" + "=" * 50)
    print("Demo 5: API Mode - JSON Direct Validation")
    print("=" * 50)
    
    examples_dir = Path(__file__).parent
    
    # Import models
    try:
        from NMIS_Ecopass.models.BatteryPass import BatteryPassport
    except ImportError:
        print("❌ BatteryPass models not found.")
        return
    
    # =========================================================================
    # 1. LOAD JSON PAYLOAD (simulating API request body)
    # =========================================================================
    print("\n1. Loading JSON payload (simulating API POST request)...")
    
    payload_path = examples_dir / "sample_api_payload.json"
    if not payload_path.exists():
        print(f"❌ Sample payload not found: {payload_path}")
        return
    
    with open(payload_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    
    print(f"   ✓ Loaded payload with {len(payload)} top-level keys")
    
    # =========================================================================
    # 2. VALIDATE AGAINST PYDANTIC MODEL
    # =========================================================================
    print("\n2. Validating against BatteryPassport Pydantic model...")
    
    try:
        passport = BatteryPassport.model_validate(payload)
        print("   ✅ Validation PASSED!")
        print(f"   • Passport ID: {passport.generalProductInformation.batteryPassportIdentifier}")
        print(f"   • Product ID: {passport.generalProductInformation.productIdentifier}")
        print(f"   • Category: {passport.generalProductInformation.batteryCategory.value}")
    except Exception as e:
        print(f"   ❌ Validation FAILED:")
        print(f"   {e}")
        return
    
    # =========================================================================
    # 3. EXPORT JSON SCHEMA (for Power Automate / OpenAPI integration)
    # =========================================================================
    print("\n3. Exporting JSON Schema for automation tools...")
    
    schema = BatteryPassport.model_json_schema()
    schema_path = examples_dir / "battery_passport_schema.json"
    
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    
    print(f"   ✓ JSON Schema saved to: {schema_path}")
    print(f"   • Title: {schema.get('title', 'N/A')}")
    print(f"   • Total definitions: {len(schema.get('$defs', {}))}")
    print("   → Import this schema into Power Automate Custom Connector")
    
    # =========================================================================
    # 4. SHOW FIELD REQUIREMENTS (required vs optional)
    # =========================================================================
    print("\n4. Field Requirements Analysis...")
    
    fields = BatteryPassport.model_fields
    required_fields = [name for name, info in fields.items() if info.is_required]
    optional_fields = [name for name, info in fields.items() if not info.is_required]
    
    print(f"   📋 Required fields ({len(required_fields)}):")
    for field in required_fields:
        print(f"      • {field}")
    
    print(f"   📋 Optional fields ({len(optional_fields)}):")
    for field in optional_fields:
        print(f"      • {field}")
    
    # =========================================================================
    # 5. COMPLIANCE PERCENTAGE TRACKER
    # =========================================================================
    print("\n5. Compliance Tracking (% of fields populated)...")
    
    def calculate_section_completeness(model_instance, model_class) -> dict:
        """Calculate field completeness for each section."""
        results = {}
        for field_name, field_info in model_class.model_fields.items():
            value = getattr(model_instance, field_name, None)
            if value is not None:
                # For nested models, check their fields too
                if hasattr(value, 'model_fields'):
                    nested_fields = value.model_fields
                    filled = sum(1 for f in nested_fields if getattr(value, f, None) is not None)
                    total = len(nested_fields)
                    results[field_name] = round(filled / total * 100, 1) if total > 0 else 100.0
                else:
                    results[field_name] = 100.0
            else:
                results[field_name] = 0.0
        return results
    
    completeness = calculate_section_completeness(passport, BatteryPassport)
    
    print("   Section Completeness:")
    for section, percentage in completeness.items():
        bar_length = int(percentage / 10)
        bar = "█" * bar_length + "░" * (10 - bar_length)
        status = "✅" if percentage >= 80 else "⚠️" if percentage >= 50 else "❌"
        print(f"   {status} {section:40s} [{bar}] {percentage:5.1f}%")
    
    overall = sum(completeness.values()) / len(completeness) if completeness else 0
    print(f"\n   📊 Overall Compliance: {overall:.1f}%")
    
    # =========================================================================
    # 6. QR CODE GENERATION
    # =========================================================================
    print("\n6. Generating QR Code for product labeling...")
    
    try:
        from NMIS_Ecopass.utils.utils import QRCodeGenerator
        
        qr_gen = QRCodeGenerator()
        
        # Create a DPP URL (this would be your company's DPP registry URL)
        dpp_url = f"https://dpp.nmis.co.uk/passports/{passport.generalProductInformation.batteryPassportIdentifier}"
        qr_path = examples_dir / "output_api_qrcode.png"
        
        qr_gen.create_qr_code(dpp_url, str(qr_path))
        print(f"   ✅ QR Code saved to: {qr_path}")
        print(f"   • Encoded URL: {dpp_url}")
        print("   → This QR code can be printed on physical battery labels")
        
    except ImportError:
        print("   ⚠️ QR code generation requires: pip install qrcode[pil]")
    except Exception as e:
        print(f"   ⚠️ QR code generation skipped: {e}")
    
    # =========================================================================
    # 7. SAVE VALIDATED OUTPUT
    # =========================================================================
    print("\n7. Exporting validated passport...")
    
    output_path = examples_dir / "output_api_validated.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(passport.model_dump_json(indent=2, exclude_none=True))
    
    print(f"   ✅ Validated passport saved to: {output_path}")
    
    # =========================================================================
    # SUMMARY FOR INDUSTRY
    # =========================================================================
    print("\n" + "─" * 50)
    print("🏭 INDUSTRY INTEGRATION SUMMARY")
    print("─" * 50)
    print("""
This demo shows how to integrate NMIS_EcoPass with automation tools:

1. POWER AUTOMATE INTEGRATION:
   • Import 'battery_passport_schema.json' as Custom Connector schema
   • POST JSON payloads from your ERP/MES to validate data
   • Receive validated passport JSON in response

2. AZURE LOGIC APPS / ZAPIER:
   • Use HTTP triggers to receive production events
   • Validate battery data against EU Battery Regulation schema
   • Auto-generate DPP on production completion

3. QR CODE LABELING:
   • Generate QR codes linking to digital passport URL
   • Print on physical battery labels per ISO/IEC 18004:2015
   • Supports IEC 61406 compliance for identification links
""")


if __name__ == "__main__":
    print("\n🚀 DPP Bridge Prototype Demo\n")
    
    try:
        demo_isa95()
        demo_csv()
        demo_stepwise()
        demo_batterypass_mapping_validation()
        demo_api_mode()  # NEW: API Mode demo for industry automation
        print("\n✅ All demos completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

