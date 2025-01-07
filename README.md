# NMIS_Ecopass
## Accelerate your Products Journey: Build, Validate and Launch DPPs with ease

`NMIS_Ecopass` is a Python package designed for creating and managing data for digital product passports by [National Manufacturing Institute Scotland](https://www.nmis.scot/) which builds upon work by [Battery Passport](https://thebatterypass.eu/) and [Tractus-X](https://eclipse-tractusx.github.io/). It includes data validation and utility functions to streamline the process of handling product-related data.

"Note: This package is under continuous development, with additional models for 'Remanufacture,' 'MaterialComposition,' and 'AdditionalData' being actively defined and added."

## Features

- Define a structured DPP model using Pydantic.
- Validate and manipulate metadata objects easily.
- Utility functions for common operations such as creating, updating, and validating metadata.
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

#### **Step 1: Import Models**

First, import the necessary classes from `NMIS_Ecopass`:

```python
from NMIS_Ecopass import (
    DigitalProductPassport as DPP,
    Metadata,
    Circularity,
    ProductIdentifier,
    CarbonFootprint,
    RepairModel,
    MaterialInformation
)
from datetime import datetime
```

#### **Step 2: Create an Instance of DPP and Its Components**

You can start by creating an instance of `DPP` and then initialize its components:

```python
# Create an empty DPP instance
DPP_instance = DPP()

# Components are automatically initialized with default factories
# You can access and modify them directly
DPP_instance.metadata.economic_operator_id = "www.nmis.scot"
DPP_instance.metadata.issue_date = datetime.now()
DPP_instance.metadata.passport_identifier = "123e4567-e89b-12d3-a456-426614174000"
DPP_instance.metadata.status = "draft"

# Add circularity information
DPP_instance.circularity.recycledContent = [{
    "preConsumerShare": {"preConsumerWasteRecycled": 30.0},
    "recycledMaterial": {
        "material": "Aluminum",
        "materialInfoURL": "https://example.com/materials/aluminum"
    },
    "postConsumerShare": {"postConsumerWasteRecycled": 20.0}
}]

# Add product identifier information
DPP_instance.productIdentifier.batchID = "BCH-20240913-001"
DPP_instance.productIdentifier.serialID = "SN-AB123456789"
DPP_instance.productIdentifier.productStatus = "original"

# Add carbon footprint information
DPP_instance.carbonFootprint.productCarbonFootprint = 100.0
```

You can now use `DPP_instance` to access and modify data for your Digital Product Passport.

### **Full Example**

Here’s a full example that demonstrates creating and adding data to a `DigitalProductPassport`:

```python
from NMIS_Ecopass import DigitalProductPassport as DPP, Metadata, Circularity, ProductIdentifier, CarbonFootprint
from datetime import datetime

# Create an empty DPP instance
DPP_instance = DPP()

# Create and assign metadata
DPP_instance.metadata = Metadata()
DPP_instance.metadata.economic_operator_id = "www.nmis.scot"
DPP_instance.metadata.issue_date = datetime.now()
DPP_instance.metadata.passport_identifier = "123e4567-e89b-12d3-a456-426614174000"
DPP_instance.metadata.status = "draft"

# Create and assign circularity
DPP_instance.circularity = Circularity()
DPP_instance.circularity.renewable_content = 25.0
# Additional circularity fields...

# Create and assign product identifier
DPP_instance.productIdentifier = ProductIdentifier()
DPP_instance.productIdentifier.batchID = "BCH-20240913-001"
DPP_instance.productIdentifier.serialID = "SN-AB123456789"

# Create and assign carbon footprint
DPP_instance.carbonFootprint = CarbonFootprint()
DPP_instance.carbonFootprint.productCarbonFootprint = 100.0
# Additional carbon footprint fields...

# Access and modify fields
print(DPP_instance.metadata.economic_operator_id)
DPP_instance.metadata.version = "2.0.0"
```

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
