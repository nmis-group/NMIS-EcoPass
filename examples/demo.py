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


if __name__ == "__main__":
    print("\n🚀 DPP Bridge Prototype Demo\n")
    
    try:
        demo_isa95()
        demo_csv()
        demo_stepwise()
        demo_batterypass_mapping_validation()
        print("\n✅ All demos completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
