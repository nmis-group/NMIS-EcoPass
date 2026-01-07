# DPP Bridge/ ReMake DPP: Product Requirements Document

### TL;DR

Manufacturing companies struggle to implement Digital Product Passports (DPPs) due to fragmented data, complex standards, and lack of integration tools. ReMake DPP is an open source Python package that enables developers to map business data to DPP standards using automated configuration tools, making DPP generation as easy as creating a PDF.

**DPP Bridge** is an open-source Python package that provides the **missing ETL layer** for the Digital Product Passport ecosystem. It transforms enterprise manufacturing data (ISA-95 B2MML, CSV, Excel) into EU-compliant Digital Product Passports using **JSON-LD as the primary output format**.

Unlike heavyweight industrial solutions or expensive SaaS platforms, DPP Bridge is:
- **SME-accessible**: Install with pip, generate DPP in 5 lines of code
- **Standards-based**: Leverages proven libraries (eg Pydantic,Bonobo ETL, PyLD, )
- **Manufacturing-native**: Built-in ISA-95 B2MML connector (unique in market)
- **Bidirectional**: Also generates ISA-95 work orders FROM DPPs (circular economy)

**Tagline:** *"The ETL layer the DPP ecosystem is missing - transform manufacturing data to EU-compliant passports in minutes, not months."*

---

## Problem Statement

### The Compliance Deadline

Manufacturing companies face mandatory Digital Product Passport regulations:
- **Battery Passport:** February 2027
- **Textile DPP:** 2027-2028
- **ESPR Generic DPP:** Rolling out 2027-2030

### The Current Gap

```
┌─────────────────┐                              ┌─────────────┐
│  Your Data      │          ?????????           │  EU DPP     │
│  ─────────────  │                              │  Registry   │
│  • MES (ISA-95) │  ──────── MISSING ────────►  │             │
│  • Spreadsheets │          TOOLING             │  QR Code    │
│  • ERP exports  │                              │  Consumer   │
└─────────────────┘                              └─────────────┘
```

### Why Existing Solutions Fall Short

| Solution | Problem |
|----------|---------|
| **BaSyx/AAS Ecosystem** | Defines data model, not transformation. Requires deep expertise. No ISA-95 integration. |
| **Catena-X** | Automotive only. Requires certification, infrastructure, membership (€€€). |
| **CIRPASS-2** | Defines requirements, not implementations. No reusable code. |
| **Commercial DPP-as-a-Service** | €10-50K/year. Vendor lock-in. Overkill for SMEs. |
| **Manual Excel/CSV** | Slow, error-prone, doesn't scale. No validation. |

### The Real Gap: No "ETL for DPP"

> *"The asset administration shell is not yet ready for the market, which makes widespread implementation difficult."*  
> — Industry expert, March 2025

**Nobody provides tools to get data INTO DPP formats from existing systems.**

---


## Goals

### Business Goals (6-12 Months)

| Goal | Metric | Target | Why It Matters |
|------|--------|--------|----------------|
| **Adoption** | PyPI downloads | 100+ | Validates market need |
| **Community** | GitHub stars | 20+ | Developer interest signal |
| **Validation** | Pilot implementations | 2+ companies | Real-world testing |
| **Ecosystem** | Listed by CIRPASS/IDTA | Yes | Legitimacy in DPP space |
| **ISA-95 Adoption** | Companies using B2MML connector | 1 | Validates differentiator |


### User Goals

* Enable users to find and use compliant DPPs from their own business data with tooling to support mapping.

* Provide intuitive tools (python package) for configuring and validating DPP data models.

* Ensure DPPs are interoperable and meet regulatory requirements.

* Offer starter kits and templates to accelerate onboarding and reduce learning curve.

### Non-Goals

* No direct connectors to ERP/PLM or other business systems in the initial release.

* No real-time or cloud-based validation; only offline, local validation is supported.

* No support for proprietary or non-standard DPP formats outside the targeted standard(s) in MVP.

---

## User Stories

### Primary Personas

#### Data-Responsible Operations Manager at an SME

This persona isn’t a DPP expert. Their job is to keep production running and address new compliance risks as they arise. They rarely know about “DPP schemas” or their obligations in detail. They need plain-language guidance, clarity on which passport types are relevant, a rapid way to check if their data is sufficient, and practical tools to close gaps.

#### User Attributes:

* Often responsible for compliance or digital innovation, but not a standards specialist.
* Has limited technical support; may rely on spreadsheets or ad hoc database exports.
* Measures success by successfully submitting compliance files with minimal disruption.
* Unsure which DPP models are official, required, or suitable for their products.

#### User Stories:

* As a Data-Responsible Manager, I want to see a list of available DPP schemas by sector so I can understand which ones apply to our products.
* As a new DPP user, I want clear badges showing which DPP schemas are “EU-verified” or “industry-accepted,” so I don’t implement a dead-end standard.
* As an operations lead, I want to upload my company’s exports and get a simple gap report, identifying what data I have, what’s missing, and what’s required by the selected DPP schema.
* As a non-expert in digital standards, I want step-by-step guidance to help me turn my existing data into a compliant DPP, so I can avoid costly mistakes or penalties.
* As a business owner, I want recommendations for filling critical data gaps (e.g., “ask your supplier for X,” or “track Y in future exports”), reducing time-to-compliance.
### Secondary Personas

**Standards Organization Representative**

* As a standards organization member, I want to review and contribute to the open source implementation, so that it aligns with evolving DPP requirements.

**Consultant**

* As a consultant, I want to use the package as a reference for client implementations, so that I can accelerate DPP adoption.

**Researcher**

* As a researcher, I want to extend the framework for new DPP standards, so that I can prototype and test emerging requirements.

---

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DPP BRIDGE                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CONNECTORS          MAPPING ENGINE              EXPORTS            │
│  ──────────          (Bonobo-based)             ───────             │
│                                                                     │
│  ┌─────────┐         ┌──────────────┐          ┌─────────────┐    │
│  │ ISA-95  │         │     YAML     │          │  JSON-LD    │    │
│  │ B2MML   │────┐    │   Mappings   │     ┌───►│  (PyLD)     │    │
│  └─────────┘    │    │              │     │    └─────────────┘    │
│                 │    │  ┌────────┐  │     │                       │
│  ┌─────────┐    │    │  │Transform│ │     │    ┌─────────────┐    │
│  │   CSV   │────┼───►│  │Registry │ ├─────┼───►│ GS1 Digital │    │
│  │  Excel  │    │    │  └────────┘  │     │    │    Link     │    │
│  └─────────┘    │    │              │     │    └─────────────┘    │
│                 │    │  Yamale      │     │                       │
│  ┌─────────┐    │    │  Validation  │     │    ┌─────────────┐    │
│  │  JSON   │────┘    └──────────────┘     └───►│    AASX     │    │
│  │   XML   │                                    │ (optional)  │    │
│  └─────────┘                                    └─────────────┘    │
│                                                                     │
│  Future - REVERSE FLOW (Circular Economy)                                   │
│  ───────────────────────────────                                   │
│  Battery DPP ──► ISA-95 Work Definition ──► MES (for repairs)     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```


## Functional Requirements

* **Data Mapping & Configuration (Priority: High)**

  * Data Mapping Tool: Allow users to map their business data files (CSV, JSON, XML) to the DPP data model.

  * Starter Kits/Templates: Provide pre-built mapping templates for the targeted DPP standard.

  * Configuration UI: Offer both CLI and web-based configuration interfaces.

* **Validation & Compliance (Priority: High)**

  * Schema Validation: Validate mapped data against the DPP standard using Pydantic or similar schema validation.

  * Error Reporting: Generate clear, actionable validation reports for users.

* **DPP Generation & Export (Priority: High)**

  * DPP Generation: Create DPPs in the required standard format (e.g., JSON-LD, XML).

  * Export Functionality: Allow users to export DPPs for submission or sharing.

* **Interoperability & Extensibility (Priority: Medium)**

  * Plugin Architecture: Enable users to add support for new standards or custom business requirements.

  * Documentation & API Reference: Comprehensive documentation for developers and contributors.

* **User Experience & Onboarding (Priority: Medium)**

  * Guided Onboarding: Step-by-step onboarding for first-time users.

  * Example Projects: Include sample data and example mappings.

---

## User Experience

**Entry Point & First-Time User Experience**

* Users discover ReMake DPP via PyPI, GitHub, or project website.

* Installation instructions guide users to install via pip.

* Guided onboarding walks users through setting up a working directory and loading sample data.

* Starter kits/templates are offered for the selected DPP standard.

**Core Experience**

* **Step 1:** User places their business data files (CSV, JSON, XML) in a designated working directory.

  * UI/UX: Clear instructions and directory structure provided.

  * Validation: Check for file presence and supported formats.

  * Success: User is notified when files are correctly loaded.

* **Step 2:** User launches the mapping tool (CLI or web UI) to map their data fields to the DPP data model.

  * UI/UX: Guided prompts in CLI or documentation.

  * Error Handling: Highlight unmapped or incompatible fields.

  * Success: User saves mapping configuration.

* **Step 3:** User runs validation on the mapped data.

  * UI/UX: Validation results displayed with clear error messages and suggestions.

  * Success: All errors resolved, user proceeds to generation.

* **Step 4:** User generates the DPP file in the required format.

  * UI/UX: Progress indicator and confirmation on completion.

  * Success: DPP file is saved/exported to output directory.

* **Step 5:** User reviews and exports the DPP for submission or sharing.

  * UI/UX: Download/export options, with links to documentation for next steps.


## Narrative

In a mid-sized manufacturing company, the IT team faces mounting pressure to comply with new Digital Product Passport (DPP) regulations. Their product data is scattered across spreadsheets and databases, and the team is overwhelmed by the complexity of mapping this data to the latest DPP standard. Manual processes are slow, error-prone, and require deep expertise in both data engineering and regulatory compliance.

With ReMake DPP, the IT developer installs the package from PyPI, documentation is clear on what are DPPs, available standards and how to use the package. They are greeted by a guided onboarding experience. Using the web UI, they quickly load their product data into a working directory and select a starter template for the relevant DPP standard. The intuitive mapping tool allows them to align their data fields with the DPP schema, while built-in validation highlights any issues before they become costly mistakes. Within hours, the team generates a fully compliant DPP file, ready for submission.

The business benefits from faster compliance, reduced risk of regulatory penalties, and a reusable framework for future product lines. The IT team is empowered to focus on value-added tasks, while the company positions itself as a leader in digital transparency and sustainability. ReMake DPP transforms a daunting compliance challenge into a streamlined, repeatable process—unlocking efficiency and peace of mind for both users and the business.



## Technical Architecture

### Package Structure

```
dpp_bridge/
├── __init__.py                   # Public API
├── core/
│   ├── bridge.py                 # Main DPPBridge class
│   ├── config.py                 # Configuration
│   └── exceptions.py             # Custom exceptions
├── connectors/
│   ├── base.py                   # BaseConnector protocol
│   ├── isa95.py                  # ISA-95 B2MML ⭐ DIFFERENTIATOR
│   ├── csv.py                    # CSV/Excel
│   └── json_xml.py               # JSON/XML with path queries
├── mapping/
│   ├── engine.py                 # Bonobo-based mapping engine ⭐
│   ├── loader.py                 # YAML loader + Yamale validation
│   ├── transforms.py             # Transform registry
│   └── validators.py             # Validation rules
├── exporters/
│   ├── jsonld.py                 # PyLD-based JSON-LD export ⭐
│   ├── gs1.py                    # GS1 Digital Link
│   └── aas.py                    # Optional AASX (BaSyx SDK)
├── models/                       # Provided by existing NMIS_Ecopass
│   ├── passports/
│   │   ├── battery.py
│   │   ├── textile.py
│   │   └── generic.py
│   └── registry.py               # Schema registry
├── reverse/
│   ├── parser.py                 # Parse incoming DPPs
│   └── isa95_work.py             # Generate ISA-95 WorkDef
├── library/
│   └── mappings/                 # Pre-built YAML mappings ⭐
│       ├── isa95/
│       ├── csv/
│       └── excel/
└── cli/
    └── main.py                   # Click-based CLI
```

## Mapping Format Specification

### Example: ISA-95 to Battery Passport

```yaml
mapping:
  name: "ISA-95 to Battery Passport"
  version: "1.0.0"
  description: "Transform B2MML production data to Battery Passport"
  
  source:
    connector: isa95        # Use ISA-95 connector
    root: MaterialLot       # Start from MaterialLot element
    
  target:
    schema: battery_passport  # Target schema from registry
    format: jsonld          # Output format

rules:
  # Simple field mapping
  - source: "MaterialLot/ID"
    target: "identification.unique_identifier"
    required: true
    
  # Type conversion
  - source: "MaterialLot/Property[@ID='capacity_ah']/Value"
    target: "performance.rated_capacity_ah"
    transform:
      type: float
    required: true
    
  # Lookup table
  - source: "MaterialLot/MaterialDefinitionID"
    target: "composition.cell_chemistry"
    transform:
      type: lookup
      table:
        MAT-NMC811: "Lithium Nickel Manganese Cobalt Oxide (NMC 811)"
        MAT-LFP: "Lithium Iron Phosphate (LFP)"
        MAT-NCA: "Lithium Nickel Cobalt Aluminum Oxide (NCA)"
    required: true
    
  # Aggregation (sum across segments)
  - source: "//SegmentResponse/Property[@ID='co2_kg']/Value"
    target: "sustainability.carbon_footprint_kg_co2"
    transform:
      type: float
    aggregate: sum
    required: true
    
  # Template
  - source: "MaterialLot/ID"
    target: "identification.manufacturer_identifier"
    transform:
      type: template
      template: "ACME-{value}"

validation:
  required:
    - identification.unique_identifier
    - composition.cell_chemistry
    - sustainability.carbon_footprint_kg_co2
  
  ranges:
    - field: performance.rated_capacity_ah
      min: 0.1
      max: 10000
```

### Transform Types

| Transform | Parameters | Example |
|-----------|-----------|---------|
| `int` | - | `"123"` → `123` |
| `float` | precision | `"123.45"` → `123.45` |
| `datetime` | input_format, output_format | `"2024-01-15T08:00:00Z"` → `"2024-01-15"` |
| `lookup` | table, default | `"MAT-NMC811"` → `"Lithium NMC 811"` |
| `template` | template | `"BAT-001"` → `"Repair work for BAT-001"` |
| `aggregate` | sum, count, collect | Multiple values → Single value |

---

## Appendix A: Competitive Analysis Details

### BaSyx Python SDK
- **Strength**: Official AAS implementation, complete metamodel
- **Weakness**: No transformation layer, steep learning curve
- **Our Position**: Use BaSyx for optional AASX export, focus on ETL

### Catena-X Digital Product Pass
- **Strength**: Full automotive ecosystem, certification, EDC connectors
- **Weakness**: Automotive-only, requires membership (€€€), months of integration
- **Our Position**: General manufacturing, SME-friendly, works in days

### Spherity Claritas
- **Strength**: Complete SaaS platform, compliance guaranteed
- **Weakness**: €10-50K/year, vendor lock-in, proprietary
- **Our Position**: Open source, self-hosted, community-driven

### CIRPASS-2 Pilots
- **Strength**: EU-funded, real pilots, standards development
- **Weakness**: Project-specific, no reusable code, ends 2027
- **Our Position**: Production-ready tool that outlives project funding

---

## Appendix B: JSON-LD Context Example

```json
{
  "@context": {
    "@vocab": "https://dpp.eu/ns#",
    "schema": "https://schema.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    
    "identifier": "schema:identifier",
    "manufacturer": {
      "@id": "schema:manufacturer",
      "@type": "@id"
    },
    "manufacturingDate": {
      "@id": "schema:productionDate",
      "@type": "xsd:date"
    },
    "carbonFootprint": {
      "@id": "dpp:carbonFootprint",
      "@type": "xsd:float"
    }
  }
}
```

---

## Appendix C: Sample B2MML Input

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ProductionResponse xmlns="http://www.mesa.org/xml/B2MML">
    <ID>PR-2024-001</ID>
    <SegmentResponse>
        <ActualStartTime>2024-01-15T08:00:00Z</ActualStartTime>
        <MaterialActual>
            <MaterialLot>
                <ID>BAT-2024-00123</ID>
                <MaterialDefinitionID>MAT-NMC811</MaterialDefinitionID>
                <Property>
                    <ID>capacity_ah</ID>
                    <Value>100.5</Value>
                </Property>
                <Property>
                    <ID>voltage</ID>
                    <Value>400</Value>
                </Property>
            </MaterialLot>
        </MaterialActual>
        <Property>
            <ID>co2_kg</ID>
            <Value>57.5</Value>
        </Property>
    </SegmentResponse>
</ProductionResponse>
```