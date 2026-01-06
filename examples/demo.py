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


if __name__ == "__main__":
    print("\n🚀 DPP Bridge Prototype Demo\n")
    
    try:
        demo_isa95()
        demo_csv()
        demo_stepwise()
        print("\n✅ All demos completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
