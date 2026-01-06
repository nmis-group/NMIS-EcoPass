# DPP Bridge: Product Requirements Document v3

## Executive Summary

**DPP Bridge** is an open-source Python package that provides the **missing ETL layer** for the Digital Product Passport ecosystem. It transforms enterprise manufacturing data (ISA-95 B2MML, CSV, Excel) into EU-compliant Digital Product Passports using **JSON-LD as the primary output format**.

Unlike heavyweight industrial solutions or expensive SaaS platforms, DPP Bridge is:
- **SME-accessible**: Install with pip, generate DPP in 5 lines of code
- **Standards-based**: Leverages proven libraries (Bonobo ETL, PyLD, Pydantic)
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

## Solution: DPP Bridge

### Core Principles

1. **ETL-First Approach**: Focus on transformation, not data models
2. **JSON-LD Primary**: Web-native, lightweight, no special infrastructure
3. **Standards-Based**: Don't reinvent - use Bonobo ETL, PyLD, BaSyx when appropriate
4. **SME Accessible**: Install with pip, generate DPP in 5 lines of code
5. **ISA-95 Native**: Built-in B2MML connector (unique differentiator)
6. **Bidirectional**: DPP → ISA-95 work orders (circular economy)
7. **AAS Optional**: Export to AASX when industrial customers require it

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
│  REVERSE FLOW (Circular Economy)                                   │
│  ───────────────────────────────                                   │
│  Battery DPP ──► ISA-95 Work Definition ──► MES (for repairs)     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Technology Stack (Leveraging Existing Libraries)

| Layer | Technology | Why This Choice |
|-------|-----------|-----------------|
| **ETL Engine** | Bonobo | Proven ETL framework, DAG execution, parallel processing |
| **JSON-LD** | PyLD | W3C standard implementation, schema.org compatible |
| **YAML Validation** | Yamale | Simple, clear error messages, schema-based |
| **XML Parsing** | lxml + xmltodict | Industry standard, XPath support, namespace handling |
| **Schema Validation** | Pydantic v2 | Type safety, clear errors, JSON Schema generation |
| **CLI** | Click | Better UX than argparse, decorator-based |
| **Optional AAS** | BaSyx Python SDK | Official AAS implementation when needed |

**Key Insight**: By using proven libraries, we save ~1,150 lines of code and gain battle-tested functionality.

### Why JSON-LD Over AAS as Primary Format?

| Aspect | JSON-LD | AAS/AASX |
|--------|---------|----------|
| **EU Compliance** | ✅ Yes (ESPR accepts "machine-readable, open format") | ✅ Yes |
| **File size** | ~5-15 KB | ~25-100 KB |
| **Web native** | ✅ Direct browser render, schema.org | ❌ Requires AAS server |
| **Infrastructure** | Static file hosting | AAS server needed |
| **Developer familiarity** | Every dev knows JSON | Niche industrial |
| **Search engines** | ✅ Google/Bing understand JSON-LD | ❌ No indexing |
| **Dependencies** | Standard library + PyLD | basyx-python-sdk |
| **When to use** | 90% of cases | Automotive tier-1, Catena-X certified |

**Decision**: JSON-LD primary, AASX optional export for industrial customers.

---

## Market Position

### Competitive Landscape

| Competitor | Type | Gap We Fill |
|-----------|------|-------------|
| **BaSyx Python SDK** | Open-source AAS library | ✅ No transformation layer, no ISA-95 |
| **Catena-X DPP** | Automotive ecosystem | ✅ Too heavy, automotive-only, requires certification |
| **Spherity Claritas** | Commercial SaaS | ✅ Expensive, vendor lock-in, no ISA-95 |
| **CIRPASS Pilots** | EU project | ✅ No reusable code, project-specific |
| **Manual Excel** | DIY approach | ✅ No validation, error-prone, doesn't scale |

### Our Unique Position

```
              Complexity/Cost
                    ↑
                    │
    Catena-X ●      │      ● Commercial DPP SaaS
    Automotive      │        (€10-50K/year)
                    │
                    │
                    │    ● DPP Bridge ← YOU ARE HERE
                    │      (Open source, SME-friendly)
    Manual Excel ●  │
    Spreadsheets    │
                    │
    ────────────────┼────────────────────────→
                    │              Manufacturing
                 Simple              Integration
```

**Sweet Spot**: Professional ETL tool without enterprise complexity or cost.

---

## Goals

### Business Goals (6 Months)

| Goal | Metric | Target | Why It Matters |
|------|--------|--------|----------------|
| **Adoption** | PyPI downloads | 1,000+ | Validates market need |
| **Community** | GitHub stars | 200+ | Developer interest signal |
| **Validation** | Pilot implementations | 5+ companies | Real-world testing |
| **Ecosystem** | Listed by CIRPASS/IDTA | Yes | Legitimacy in DPP space |
| **ISA-95 Adoption** | Companies using B2MML connector | 10+ | Validates differentiator |

### User Goals

| Persona | Goal | Success Metric |
|---------|------|----------------|
| **Manufacturing IT Developer** | Generate DPP from MES data | < 2 hours from install to first DPP |
| **Product Data Manager** | Configure mappings without coding | YAML-only configuration, no Python |
| **Sustainability Officer** | Validate EU compliance | Clear pass/fail report with errors |
| **Remanufacturer** | Generate work orders from DPP | Automated ISA-95 output |
| **SME Owner** | Quick compliance | Working DPP in 1 day, not 1 month |

### Technical Goals

| Goal | Target | Validation |
|------|--------|------------|
| **Performance** | Transform 10K records in <10 seconds | Benchmark tests |
| **Reliability** | 99%+ transform success rate | Integration tests |
| **Usability** | Non-developer can use CLI | User testing |
| **Compatibility** | Works on Win/Mac/Linux, Python 3.10+ | CI/CD matrix |
| **Extensibility** | Add new DPP type in <2 hours | Developer survey |

### Non-Goals (v1.0)

- ❌ Real-time streaming / live telemetry (batch only)
- ❌ Cloud-hosted service (local/self-hosted only)
- ❌ Web UI (CLI and Python API only)
- ❌ Direct ERP connectors (users export to CSV/XML first)
- ❌ Blockchain / verifiable credentials (future consideration)
- ❌ Data warehousing features (transformation only)

---

## User Stories

### Epic 1: Data Import

```
US-1.1: ISA-95 B2MML Import (PRIORITY 1)
As a manufacturing IT developer
I want to parse ISA-95 B2MML XML files from our MES
So I can extract production data for DPP generation
Acceptance: Parse MaterialLot, ProductionResponse, SegmentResponse

US-1.2: CSV/Excel Import
As a product data manager
I want to load spreadsheet-based product data
So I can work with our existing data exports
Acceptance: Auto-detect delimiters, handle multiple sheets

US-1.3: JSON/XML Import
As a developer
I want to load generic JSON/XML with path queries
So I can extract data from various export formats
Acceptance: JSONPath and XPath support
```

### Epic 2: Mapping & Transformation (CORE VALUE)

```
US-2.1: YAML Mapping Configuration
As a product data manager
I want to define mappings in YAML without coding
So non-developers can modify transformations
Acceptance: Declarative syntax, validation with Yamale

US-2.2: Built-in Transformations
As a developer
I want built-in transforms (type coercion, lookups, templates)
So I can handle real-world data without custom code
Acceptance: int, float, datetime, lookup, template, aggregate

US-2.3: Pre-built Mapping Templates
As an SME owner
I want to use ready-made mapping templates
So I don't start from scratch
Acceptance: 5+ templates for common scenarios (ISA-95→Battery, CSV→Textile)

US-2.4: Validation Rules
As a compliance officer
I want to validate required fields and data ranges
So I catch errors before submission
Acceptance: Required fields, type checking, value ranges
```

### Epic 3: DPP Generation (OUTPUT)

```
US-3.1: JSON-LD Export (Primary)
As a developer
I want to export JSON-LD with proper context
So DPPs work natively on the web
Acceptance: Uses PyLD, includes @context, validates structure

US-3.2: GS1 Digital Link URLs
As a product manager
I want GS1 Digital Link URLs for QR codes
So consumers can scan products
Acceptance: Generate URLs, optional QR code images

US-3.3: EU Schema Validation
As a compliance officer
I want to validate against EU schemas
So I catch compliance errors before submission
Acceptance: Pydantic validation, clear error messages

US-3.4: Optional AASX Export
As an automotive tier-1 supplier
I want to export AASX for Catena-X
So I can integrate with certified systems
Acceptance: Uses BaSyx SDK, optional dependency
```

### Epic 4: Reverse Flow (CIRCULAR ECONOMY)

```
US-4.1: Parse Incoming DPPs
As a remanufacturer
I want to parse incoming DPPs
So I can access serviceability information
Acceptance: Read JSON-LD, extract repair data

US-4.2: Generate ISA-95 Work Definitions
As a remanufacturer
I want to generate ISA-95 Work Definitions
So repair planning integrates with my MES
Acceptance: Output B2MML XML, material requirements, work segments
```

### Epic 5: Developer Experience

```
US-5.1: Simple CLI
As a developer
I want a simple CLI for quick transformations
So I can test without writing code
Acceptance: `dpp-bridge transform input.xml -m mapping.yaml -o output.json`

US-5.2: Python API
As a Python developer
I want a clean Python API
So I can integrate DPP generation into my applications
Acceptance: 5-line example works

US-5.3: Clear Error Messages
As any user
I want clear error messages when things fail
So I can fix problems quickly
Acceptance: Actionable errors, line numbers for YAML errors
```

---

## Functional Requirements

### FR1: Connectors (Priority: High)

| ID | Requirement | Implementation | Dependencies |
|----|-------------|----------------|--------------|
| FR1.1 | ISA-95 B2MML Parser | Parse MaterialLot, ProductionResponse, ProcessSegment with lxml + XPath | lxml, xmltodict |
| FR1.2 | ISA-95 B2MML Generator | Generate WorkDefinition for reverse flow | lxml |
| FR1.3 | CSV Connector | Auto-detect delimiters, headers, encodings | csv (stdlib) |
| FR1.4 | Excel Connector | Support .xlsx, multiple sheets | openpyxl |
| FR1.5 | JSON/XML Connector | JSONPath and XPath query support | lxml, jsonpath-ng |

**Acceptance Criteria:**
- Parse sample B2MML file in <1 second
- Handle namespace variations
- Graceful error handling for malformed XML

### FR2: Schemas (Priority: High)

| ID | Requirement | Source | Format |
|----|-------------|--------|--------|
| FR2.1 | Battery Passport | EU Battery Regulation 2023/1542 | Pydantic model |
| FR2.2 | Textile DPP | CIRPASS textile requirements | Pydantic model |
| FR2.3 | Generic ESPR DPP | Base schema for other product categories | Pydantic model |
| FR2.4 | Schema Validation | Validation with clear error messages | Pydantic v2 |
| FR2.5 | Schema Registry | Pluggable schema system | Custom registry |

**Acceptance Criteria:**
- All EU mandatory fields present
- Validation errors show field path and issue
- Easy to add new schemas (<100 LOC)

### FR3: Export Formats (Priority: High)

| ID | Requirement | Technology | Status |
|----|-------------|-----------|---------|
| FR3.1 | JSON-LD Export | PyLD library | Primary format |
| FR3.2 | GS1 Digital Link | URL generation | Core feature |
| FR3.3 | JSON Schema Output | For downstream validation | Optional |
| FR3.4 | AASX Export | BaSyx Python SDK | Optional (`pip install dpp-bridge[aas]`) |
| FR3.5 | QR Code Generation | qrcode library | Optional (`pip install dpp-bridge[qr]`) |

**Acceptance Criteria:**
- JSON-LD validates with Google Structured Data Testing Tool
- File size <50KB for typical DPP
- AASX only installed when needed

### FR4: Mapping Engine (Priority: Critical)

| ID | Requirement | Technology | Priority |
|----|-------------|-----------|----------|
| FR4.1 | YAML Configuration | PyYAML + Yamale validation | P0 |
| FR4.2 | Field Mapping | Source path → target path with Bonobo nodes | P0 |
| FR4.3 | Transforms | String, int, float, datetime, lookup, template | P0 |
| FR4.4 | Aggregations | Sum, count, collect for multi-record sources | P1 |
| FR4.5 | Validation Rules | Required fields, ranges, formats with Pydantic | P0 |
| FR4.6 | Parallel Execution | Bonobo graph execution | P1 |

**Acceptance Criteria:**
- Process 10K records in <10 seconds
- YAML validation errors show line numbers
- Transform errors don't crash entire pipeline

### FR5: CLI (Priority: High)

| ID | Command | Example | Priority |
|----|---------|---------|----------|
| FR5.1 | Transform | `dpp-bridge transform -m mapping.yaml input.xml` | P0 |
| FR5.2 | Validate | `dpp-bridge validate mapping.yaml` | P0 |
| FR5.3 | Inspect | `dpp-bridge inspect input.xml` (detect schema) | P1 |
| FR5.4 | QR | `dpp-bridge qr passport.json --output qr.png` | P2 |
| FR5.5 | List Schemas | `dpp-bridge list-schemas` | P1 |

**Acceptance Criteria:**
- Follows UNIX conventions (stdin/stdout)
- Progress bars for long operations
- Exit codes: 0 success, 1 error

---

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

### Dependencies

```toml
[project]
name = "dpp-bridge"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    # Core ETL
    "bonobo>=0.6.3",              # ETL graph execution
    
    # Data validation
    "pydantic>=2.0",              # Schema validation
    "yamale>=4.0",                # YAML validation
    
    # File parsing
    "pyyaml>=6.0",                # YAML parsing
    "lxml>=4.9",                  # XML/XPath (ISA-95)
    "xmltodict>=0.13",            # Easier XML navigation
    "openpyxl>=3.1",              # Excel support
    
    # JSON-LD
    "pyld>=2.0.3",                # W3C JSON-LD processor
    
    # CLI
    "click>=8.0",                 # Command-line interface
]

[project.optional-dependencies]
aas = ["basyx-python-sdk>=1.0.0"]  # AAS/AASX export
qr = ["qrcode[pil]>=7.0"]          # QR code generation
dev = ["pytest>=7.0", "pytest-cov>=4.0", "ruff>=0.1"]
```

### Data Flow

```
1. INPUT
   ├─ ISA-95 XML ──────┐
   ├─ CSV ─────────────┤
   └─ Excel ───────────┘
                        ↓
2. CONNECTOR (lxml/csv)
   Returns: Iterator[Dict[str, Any]]
                        ↓
3. MAPPING ENGINE (Bonobo Graph)
   ├─ Load YAML (Yamale validates)
   ├─ Apply transforms (TransformRegistry)
   └─ Build nested dict
                        ↓
4. VALIDATION (Pydantic)
   Validates: BatteryPassport | TextileDPP | GenericDPP
                        ↓
5. EXPORT (PyLD)
   ├─ JSON-LD (primary) ──────┐
   ├─ GS1 Digital Link ────────┤
   └─ AASX (optional) ─────────┘
                               ↓
6. OUTPUT
   passport.json (5-15KB)
```

### Key Design Decisions

| Decision | Rationale | Alternative Considered |
|----------|-----------|------------------------|
| **Bonobo for ETL** | Proven framework, parallel execution, clean API | Custom engine (reinventing wheel) |
| **PyLD for JSON-LD** | W3C standard, schema.org compatible | Manual @context handling (error-prone) |
| **Yamale for YAML** | Simple, great errors | pykwalify (more complex) |
| **Pydantic v2** | Type safety, JSON Schema generation | Marshmallow (less type safety) |
| **Click for CLI** | Better UX than argparse | Typer (more magic) |
| **JSON-LD primary** | Web-native, lightweight | AAS-first (too heavy) |

---

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

## Roadmap

### Phase 1: MVP (Weeks 1-4) ✅ FOUNDATION

**Goal**: Working ISA-95 → Battery DPP transformation

| Week | Deliverable | Technology |
|------|-------------|-----------|
| 1 | ISA-95 B2MML connector | lxml, xmltodict |
| 2 | Mapping engine with Bonobo | Bonobo, Yamale |
| 3 | JSON-LD export + CLI | PyLD, Click |
| 4 | CSV connector + tests | csv, pytest |

**Exit Criteria:**
- ✅ Can transform ISA-95 → Battery DPP (JSON-LD)
- ✅ Can transform CSV → Textile DPP (JSON-LD)
- ✅ CLI works: `dpp-bridge transform input.xml -m mapping.yaml -o output.json`
- ✅ 80%+ test coverage

### Phase 2: Production Ready (Weeks 5-8) 📚 POLISH

**Goal**: Professional package ready for PyPI

| Week | Deliverable |
|------|-------------|
| 5-6 | Pre-built mapping library (5+ templates) |
| 7 | GS1 Digital Link + QR codes |
| 8 | Documentation + PyPI release |

**Exit Criteria:**
- ✅ 5+ pre-built mappings (ISA-95→Battery, CSV→Textile, etc.)
- ✅ Documentation site with tutorials
- ✅ Published to PyPI: `pip install dpp-bridge`
- ✅ 3+ example projects

### Phase 3: Reverse Flow (Weeks 9-12) ♻️ CIRCULAR ECONOMY

**Goal**: DPP → ISA-95 work orders

| Week | Deliverable |
|------|-------------|
| 9-10 | DPP parser (JSON-LD → dict) |
| 11-12 | ISA-95 Work Definition generator |

**Exit Criteria:**
- ✅ Parse Battery DPP serviceability data
- ✅ Generate ISA-95 WorkDefinition XML
- ✅ End-to-end repair scenario demo

### Phase 4: Ecosystem (Weeks 13-16) 🌍 GROWTH

**Goal**: Community adoption and ecosystem integration

| Week | Deliverable |
|------|-------------|
| 13 | Optional AASX export (BaSyx SDK) |
| 14 | Plugin system for custom connectors |
| 15 | CIRPASS-2 / IDTA outreach |
| 16 | Community mapping contributions |

**Exit Criteria:**
- ✅ Listed on CIRPASS-2 tools page
- ✅ 10+ community-contributed mappings
- ✅ 200+ GitHub stars

---

## Success Metrics

### Leading Indicators (1-3 Months)

| Metric | Target | Validation |
|--------|--------|------------|
| GitHub stars | 50+ | Community interest |
| PyPI downloads/month | 300+ | Actual usage |
| Documentation page views | 1000+ | Developer interest |
| Test coverage | 85%+ | Code quality |
| CLI command success rate | 99%+ | Reliability |

### Lagging Indicators (3-6 Months)

| Metric | Target | Validation |
|--------|--------|------------|
| Pilot companies | 5+ | Real-world validation |
| ISA-95 connector usage | 10+ companies | Differentiator adoption |
| GitHub stars | 200+ | Growing community |
| PyPI downloads/month | 1000+ | Market adoption |
| Community mappings | 10+ | Ecosystem health |

### Qualitative Success

- ✅ Featured on CIRPASS-2 tools list
- ✅ Referenced in ISA-95 community
- ✅ Users report "<2 hours to first DPP"
- ✅ SMEs prefer DPP Bridge over commercial tools
- ✅ Contributors from multiple companies

---

## Risk Management

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| EU schema changes before regulation | Medium | Medium | Abstract schema layer, version pinning, registry system |
| ISA-95 assumption wrong (users have CSV only) | Medium | Low | CSV connector equally prioritized, both work well |
| Bonobo performance issues | Low | Low | Benchmark early, fallback to custom engine |
| PyLD compatibility issues | Low | Low | W3C standard, mature library |

### Market Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low adoption (no market need) | High | Medium | Partner with NMIS network, target EcoMatter users |
| Commercial vendors undercut price | Medium | Medium | Open source can't be undercut, focus on quality |
| AAS becomes mandatory | Low | Low | Optional AASX export already planned |
| Catena-X dominates all sectors | Medium | Low | They're automotive-only, we're general manufacturing |

### Execution Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Developer capacity shortage | High | Medium | Clear requirements doc, junior dev can execute |
| Scope creep (too many features) | Medium | High | Strict non-goals, phase-based delivery |
| Documentation lags behind code | Medium | Medium | Docs in Phase 2, examples in Phase 3 |
| No pilot companies | High | Low | NMIS network access, Scottish textile contacts |

---

## Go-to-Market Strategy

### Target Segments (Priority Order)

1. **Scottish Manufacturing SMEs** (via NMIS network)
   - Textiles, food & beverage, machinery
   - Pain: Manual compliance processes
   - Message: "Scottish-built DPP tool for manufacturers"

2. **EcoMatter Users** (existing NMIS DPP community)
   - Already building DPPs, need better tooling
   - Pain: Current tools too complex
   - Message: "The ETL layer you've been missing"

3. **Manufacturing IT Consultants**
   - Need tools for client projects
   - Pain: Building custom solutions
   - Message: "Professional DPP ETL in your toolkit"

4. **EU DPP Pilot Projects** (CIRPASS-2, IDTA members)
   - Testing DPP implementations
   - Pain: Lack of transformation tools
   - Message: "Open source, standards-based, production-ready"

### Launch Strategy

**Week 1-4: Soft Launch**
- Private beta with 2-3 NMIS companies
- GitHub repo public, PyPI test deployment
- Gather feedback, iterate

**Week 5-8: Public Launch**
- PyPI official release
- Blog post: "Announcing DPP Bridge"
- LinkedIn posts in manufacturing groups
- ISA-95 mailing list announcement

**Week 9-12: Ecosystem Building**
- CIRPASS-2 working group presentation
- IDTA tools showcase submission
- ISA-95 committee demo
- First community mapping contributions

### Distribution Channels

1. **PyPI** (primary) - `pip install dpp-bridge`
2. **GitHub** - Source code, issues, discussions
3. **Documentation Site** - Tutorials, examples, API docs
4. **NMIS Network** - Direct outreach to member companies
5. **LinkedIn** - Manufacturing IT groups, DPP discussions
6. **ISA-95 Community** - Mailing lists, working groups

---

## Open Questions & Decisions Needed

### Naming

**Options:**
1. `dpp-bridge` (current) - Clear purpose, search-friendly
2. `dpp-transform` - More descriptive
3. `ecopass-etl` - Leverages NMIS EcoPass brand

**Recommendation**: Keep `dpp-bridge` - it's distinctive and describes role.

### Governance

**Options:**
1. Personal project (Awais maintains)
2. NMIS project (institutional backing)
3. Apache/Eclipse foundation (neutral governance)

**Recommendation**: Start personal, move to NMIS after pilot validation.

### First Pilot Partner

**Options:**
1. Scottish textile manufacturer (knows Awais)
2. NMIS member with MES system
3. EcoMatter active user

**Recommendation**: Scottish textile manufacturer - easiest to secure, real pain point.

### GS1 Partnership

**Question**: Worth pursuing for resolver network access?

**Consideration**: GS1 Digital Link is open standard, don't need partnership for basic implementation. Revisit if users need official resolver registration.

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

---

## Appendix D: Development Team

**Required Skills:**
- Python 3.10+ (intermediate level)
- XML/XPath (basics)
- YAML (basics)
- Git/GitHub

**Nice to Have:**
- Manufacturing systems knowledge
- ETL experience
- Pydantic experience

**Estimated Effort:**
- 1 junior Python developer, full-time
- 8-12 weeks for Phase 1-3
- Part-time senior dev for code review

**Total**: ~400 hours of development

---

**Document Version**: 3.0  
**Last Updated**: January 2026  
**Author**: Awais Hassan Munawar (NMIS)  
**Status**: Ready for Development