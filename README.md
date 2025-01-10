# NMIS_Ecopass
## Accelerate your Products Journey: Build, Validate and Launch DPPs with ease

`NMIS_Ecopass` is a Python package designed for creating and managing data for digital product passports by [National Manufacturing Institute Scotland](https://www.nmis.scot/) which builds upon work by [Battery Passport](https://thebatterypass.eu/) and [Tractus-X](https://eclipse-tractusx.github.io/). It includes data validation and utility functions to streamline the process of handling product-related data.

"Note: This package is under continuous development and will appreciate any contributions to the models."

## Features

- Define a structured DPP model using Pydantic.
- Validate and manipulate objects easily.
- Utility functions for common operations such as creating industrial QR codes based on ISO 61406.
- Comprehensive models for material composition, remanufacturing, and circularity tracking.
- Carbon footprint tracking across product lifecycle stages.


## **Table of Contents**
1. [Installation](#installation)
2. [Quick Start Guide](#quick-start-guide)
3. [Creating a Digital Product Passport (DPP)](#creating-a-digital-product-passport-dpp)
    - [Step 1: Import Models](#step-1-import-models)
    - [Step 2: Create an Instance of DPP and Its Components](#step-2-create-an-instance-of-dpp-and-its-components)
4. [Full Example](#full-example)
5. [Model Details](#model-details)
    - [Metadata](#metadata)
    - [Product Identifier](#product-identifier)
    - [Circularity](#circularity)
    - [Carbon Footprint](#carbon-footprint)
    - [Material Information](#material-information)
    - [Remanufacture](#remanufacture)
6. [Contributing](#contributing)
7. [License](#license)



## Installation

Install the package using pip:

```bash
pip install NMIS_Ecopass
```

## **Quick Start Guide**

This guide will show you how to create a Digital Product Passport (DPP) using the models provided in the `NMIS_Ecopass`.

### **Creating a Digital Product Passport (DPP)**

You can create a DPP either by providing all data at once or by building it incrementally. Here's how to build it step by step:

```python
from datetime import datetime
import uuid
from NMIS_Ecopass.models import *

# Create empty DPP instance
DPP_instance = DigitalProductPassport()

# Step 1: Add Metadata
DPP_instance.metadata = Metadata()
DPP_instance.metadata.economic_operator_id = "company.com"
DPP_instance.metadata.registration_identifier = "https://www.eco123.company.com"
DPP_instance.metadata.issue_date = datetime.now()
DPP_instance.metadata.status = StatusEnum.ACTIVE
DPP_instance.metadata.version = "1.0.0"
DPP_instance.metadata.passport_identifier = uuid.uuid4()

# Step 2: Add Product Identification
DPP_instance.productIdentifier = ProductIdentifier()
DPP_instance.productIdentifier.batchID = "BATCH-001"
DPP_instance.productIdentifier.serialID = "SN-001"
DPP_instance.productIdentifier.productStatus = ProductStatus.ORIGINAL
DPP_instance.productIdentifier.productName = "Your Product Name"

# Step 3: Add Circularity Information
DPP_instance.circularity = Circularity()
recycled_content = RecycledContent(
    preConsumerShare=45.0,
    recycledMaterial=RecycledMaterialInfo(
        material=RecycledMaterial.ALUMINUM,
        materialInfoURL="https://example.com/materials/aluminum-info"
    ),
    postConsumerShare=30.5
)
DPP_instance.circularity.recycledContent = [recycled_content]

# Add dismantling documentation
dismantling_doc = DismantlingAndRemovalDocumentation(
    documentType=DocumentType.DISMANTLINGMANUAL,
    mimeType=MimeType.PDF,
    documentURL=ResourcePath(
        resourcePath="https://example.com/documents/manual.pdf"
    )
)
DPP_instance.circularity.dismantlingAndRemovalInformation = [dismantling_doc]

# Step 4: Add Carbon Footprint
DPP_instance.carbonFootprint = CarbonFootprint()
lifecycle_footprint = LifecycleStageCarbonFootprint(
    lifecycleStage=LifecycleStage.RAWMATERIALEXTRACTION,
    carbonFootprint=20.0
)
DPP_instance.carbonFootprint.carbonFootprintPerLifecycleStage = [lifecycle_footprint]

# Step 5: Add Material Information
DPP_instance.productMaterial = ProductMaterial()
DPP_instance.productMaterial.productId = "PROD-001"

material_info = MaterialInformation(
    materialId="MAT-001",
    tradeName="Eco-Aluminum",
    materialCategory="metal",
    materialStandard=MaterialStandard.ISO,
    standardDesignation="AL6061-T6",
    composition=[
        {"element": "Al", "percentage": 97.5, "unit": "weight_percent"},
        {"element": "Mg", "percentage": 1.0, "unit": "weight_percent"}
    ],
    properties=[
        {"propertyName": "density", "value": 2.7, "unit": "g/cm3"}
    ],
    traceability=MaterialTraceability(
        batchNumber="BATCH-001",
        url="https://example.com/traceability/BATCH-001"
    )
)
DPP_instance.productMaterial.components = {"main_body": material_info}
DPP_instance.productMaterial.totalMass = 2.5

# Step 6: Add Remanufacturing Information
DPP_instance.reManufacture = RepairModel()
DPP_instance.reManufacture.repairId = "REP-001"
DPP_instance.reManufacture.currentCondition = ComponentCondition.SERVICEABLE

# Add repair history
repair = RepairHistory(
    repairId="RH-001",
    repairDate=datetime.now(),
    repairType=RepairType.SURFACE_TREATMENT,
    facility="Service Center",
    description="Initial inspection"
)
DPP_instance.reManufacture.repairHistory = [repair]

# Step 7: Add Additional Data (Optional)
DPP_instance.additionalData = AdditionalData(
    data_type="quality_metrics",
    data={
        "quality_score": 95,
        "certifications": ["ISO 9001", "CE Mark"]
    }
)
```

### Key Components Overview

Each section of the DPP serves a specific purpose:

1. **Metadata**: Administrative information about the passport itself
   - Economic operator identification
   - Issue and expiration dates
   - Version control
   - Status tracking

2. **Product Identifier**: Basic product information
   - Batch and serial numbers
   - Product status (original, repaired, etc.)
   - Product name and description

3. **Circularity**: Recycling and end-of-life information
   - Recycled content percentages
   - Dismantling instructions
   - End-of-life handling
   - Supplier information

4. **Carbon Footprint**: Environmental impact data
   - Carbon footprint per lifecycle stage
   - Overall product carbon footprint
   - Study documentation

5. **Material Information**: Detailed material composition
   - Material identification
   - Chemical composition
   - Physical properties
   - Traceability information

6. **Remanufacture**: Repair and maintenance tracking
   - Current condition
   - Repair history
   - Defect information
   - Test results

7. **Additional Data**: Custom extensions
   - Quality metrics
   - Certifications
   - Custom test results


### **Model Details**

#### **Metadata**
- **`backup_reference`**: Optional URL to a backup version of the DPP
- **`registration_identifier`**: URL linking to the official registration
- **`economic_operator_id`**: Identifier for the economic operator
- **`last_modification`**: Timestamp of the last modification
- **`predecessor`**: Optional reference to the previous version
- **`issue_date`**: Date when the DPP was issued
- **`version`**: Internal version number
- **`passport_identifier`**: Unique UUID4 identifier
- **`status`**: Current status (draft, active, inactive, expired)
- **`expiration_date`**: Optional expiration date

#### **Product Identifier**
- **`batchID`**: Batch identifier for products manufactured under similar conditions
- **`serialID`**: Unique product identifier
- **`productStatus`**: Current status (original, repaired, maintained, remanufactured, recycled)

#### **Circularity**
- **`dismantlingAndRemovalInformation`**: Documentation for dismantling and removal
- **`recycledContent`**: Information about pre-consumer and post-consumer recycled materials
- **`endOfLifeInformation`**: Details about waste prevention and collection
- **`supplierInformation`**: Supplier details including contact information

#### **Carbon Footprint**
- **`carbonFootprintPerLifecycleStage`**: Carbon footprint for each lifecycle stage
- **`carbonFootprintStudy`**: URL to detailed carbon footprint documentation
- **`productCarbonFootprint`**: Total product carbon footprint
- **`carbonFootprintPerformanceClass`**: Performance classification

#### **Material Information**
- **`materialId`**: Unique material identifier
- **`tradeName`**: Commercial name of the material
- **`materialCategory`**: Category (metal, polymer, ceramic, etc.)
- **`composition`**: Detailed chemical composition
- **`properties`**: Physical and mechanical properties
- **`certifications`**: Material certifications
- **`traceability`**: Batch and manufacturing information
- **`sustainability`**: Recycled content and environmental impact

#### **Remanufacture**
- **`repairId`**: Unique repair identifier
- **`componentInfo`**: Component details
- **`currentCondition`**: Assessment of current condition
- **`defects`**: Identified defects and their details
- **`processSteps`**: Repair process documentation
- **`testResults`**: Test and inspection results
- **`certification`**: Repair certification information

## **Contributing**

If you want to contribute to the `NMIS_Ecopass`, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


### Common Data Mapping Scenarios

1. **Manufacturing Data**
   - Batch/Serial numbers → `productIdentifier`
   - Material specs → `productMaterial`
   - Quality certificates → `additionalData`

2. **Maintenance Records**
   - Repair history → `reManufacture.repairHistory`
   - Inspection results → `reManufacture.testResults`
   - Service schedules → `reManufacture.nextMaintenanceDue`

3. **Sustainability Data**
   - Carbon footprint → `carbonFootprint`
   - Recycled content → `circularity.recycledContent`
   - End-of-life instructions → `circularity.dismantlingAndRemovalInformation`
