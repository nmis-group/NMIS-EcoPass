# NMIS_Ecopass Developer Guide

Welcome to the **NMIS_Ecopass** project! This guide is designed to help you understand the codebase, its architecture, and the current state of development.

## 1. Project Overview

**NMIS_Ecopass** is a Python package for creating, validating, and managing Digital Product Passports (DPP). It serves as a bridge to transform manufacturing data (from CSV, Excel, XML, etc.) into EU-compliant JSON-LD digital passports.

### Core Philosophy
- **ETL Pattern**: Extracts data from sources, Transforms it using a mapping schema, and Loads/Exports it to a destination format.
- **Model-Driven**: Uses rigid Pydantic models to ensure data validity against DPP standards.
- **Configurable**: Mappings are defined in YAML, allowing non-developers to define data transformations.

## 2. Architecture & Key Components

The source code is located in `src/NMIS_Ecopass`. Here are the main modules:

### 2.1. Core (`src/NMIS_Ecopass/core`)
- **`DPPBridge`**: The main entry point. Orchestrates the ETL process.
  - usage: `bridge = DPPBridge(); bridge.transform(...)`
- **`pipeline.py` / `bridge.py`**: Handles the flow of data.

### 2.2. Models (`src/NMIS_Ecopass/models`)
Contains Pydantic models defining the DPP structure.
- **`ReMakeDPP`**: Submodule containing the actual model definitions (e.g., `metadata.py`, `circularity.py`).
  - *Note*: Currently these are nested in `ReMakeDPP`, so imports might be tricky (see "Known Issues").
- **`registry.py`**: Manages different passport schemas.

### 2.3. Mapping Engine (`src/NMIS_Ecopass/mapping`)
Responsible for transforming raw input data into the DPP structure.
- **`engine.py`**: Executes the transformation logic.
- **`loader.py`**: Loads and validates YAML mapping files (using `yamale`).
- **`transforms.py`**: A registry of helper functions (e.g., date formatting, string cleaning) callable from the YAML mapping.

### 2.4. Connectors (`src/NMIS_Ecopass/connectors`)
Adapters for different input data formats.
- **`base.py`**: Abstract base class for all connectors.
- **Implemented**: `CSVConnector`, `ExcelConnector`, `ISA95Connector` (XML).

### 2.5. Exporters (`src/NMIS_Ecopass/exporters`)
Handles the output format.
- **`jsonld.py`**: Exports the final object to JSON-LD format.

## 3. Current Status: What's Been Done

The core functionality of the "DPP Bridge" prototype is implemented:

- [x] **ETL Pipeline**: Functional `DPPBridge` class that can Extract, Map, and Export.
- [x] **Data Ingestion**: Support for CSV, Excel, and ISA-95 XML files.
- [x] **Mapping System**: flexible YAML-based mapping system that supports nested objects and lists.
- [x] **Validation**: 
  - Input mapping validation (via `yamale` schemas).
  - Output data validation (via Pydantic models).
- [x] **Domain Models**: Comprehensive Pydantic models for Battery and Textile DPPs (in `ReMakeDPP`).
- [x] **Examples**: `demo.py` showing end-to-end usage.

## 4. Work Remaining: What Needs to be Done

There are several areas identified for immediate improvement and future development:

### 4.1. Critical Fixes (High Priority)
- **Fix Import Structure**: The `tests/test_digital_product_passport.py` fails because it imports validation models from `NMIS_Ecopass.models` directly, but the files reside in `NMIS_Ecopass/models/ReMakeDPP/`.
  - *Action*: Either move files up from `ReMakeDPP` to `models`, or update `models/__init__.py` to expose them.
- **Fix Empty `__init__.py`**: `src/NMIS_Ecopass/models/__init__.py` is currently empty, causing `import *` to fail.

### 4.2. Testing (Medium Priority)
- **Expand Test Coverage**: Currently only `test_digital_product_passport.py` exists (and is failing).
  - *Action*: Create unit tests for `CSVConnector`, `ExcelConnector`, and the `MappingEngine` specifically.
  - *Action*: Add integration tests using the example data in `examples/`.

### 4.3. Features & Refactoring (Low Priority)
- **Connector Extensibility**: Add support for SQL (SQLAlchemy) or REST API data sources.
- **Documentation**: Provide auto-generated API docs (e.g., Sphinx/MkDocs) for the Pydantic models.
- **Package Polish**: Ensure `poetry build` creates a clean distribution with all necessary non-code assets (schemas, config files).

## 5. Getting Started

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Run the Demo**:
   ```bash
   python examples/demo.py
   ```

3. **Run Tests**:
   ```bash
   pytest tests/
   ```
   *(Note: Expect failures until imports are fixed)*

4. **Explore mappings**:
   Check `examples/csv_to_textile.yaml` to see how to map CSV columns to DPP fields.
