# NMIS_Ecopass
## Accelerate your Products Journey: Build, Validate and Launch DPPs with ease

`NMIS_Ecopass` is a Python package designed for creating and managing data for digital product passports by [National Manufacturing Institute Scotland](https://www.nmis.scot/) which builds upon work by [Battery Passport](https://thebatterypass.eu/) and [Tractus-X](https://eclipse-tractusx.github.io/). It includes data validation and utility functions to streamline the process of handling product-related data.

"Note: This package is under continuous development, with additional models for 'Remanufacture,' 'MaterialComposition,' and 'AdditionalData' being actively defined and added."

## Features

- Define a structured DPP model using Pydantic.
- Validate and manipulate metadata objects easily.
- Utility functions for common operations such as creating, updating, and validating metadata.


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
from NMIS_Ecopass import DigitalProductPassport as DPP, Metadata, Circularity, ProductIdentifier, CarbonFootprint
from datetime import datetime
```

#### **Step 2: Create an Instance of DPP and Its Components**

You can start by creating an instance of `DPP` and then initialize its components (`Metadata`, `Circularity`, `ProductIdentifier`, `CarbonFootprint`) as follows:

```python
# Create an empty DPP instance
DPP_instance = DPP()

# Initialize components
DPP_instance.metadata = Metadata()
DPP_instance.circularity = Circularity()
DPP_instance.productIdentifier = ProductIdentifier()
DPP_instance.carbonFootprint = CarbonFootprint()
```

Now, you can add data to each component:

```python
# Add metadata information
DPP_instance.metadata.economic_operator_id = "www.nmis.scot"
DPP_instance.metadata.issue_date = datetime.now()
DPP_instance.metadata.passport_identifier = "123e4567-e89b-12d3-a456-426614174000"
DPP_instance.metadata.status = "draft"

# Add circularity information
DPP_instance.circularity.renewable_content = 30.0
# Additional fields can be added similarly

# Add product identifier information (Example fields, replace with actual)
DPP_instance.productIdentifier.batchID = "BCH-20240913-001"
DPP_instance.productIdentifier.serialID = "SN-AB123456789"

# Add carbon footprint information (Example fields, replace with actual)
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
- **`backup_reference`**: Optional URL to a backup version of the DPP.
- **`registration_identifier`**: URL linking to the official registration of the DPP.
- **`economic_operator_id`**: Identifier for the economic operator (e.g., tax code).
- **`last_modification`**: Timestamp of the last modification.
- **`predecessor`**: Optional reference to the previous version of the DPP.
- **`issue_date`**: Date when the DPP was issued.
- **`version`**: Internal version number for the DPP.
- **`passport_identifier`**: Unique UUID4 identifier for the product passport.
- **`status`**: Current status of the metadata (e.g., draft, active, inactive, expired).
- **`expiration_date`**: Optional date when the DPP will expire.

#### **Product Identifier**
- **`batchID`**: Unique batch identifier for the product.
- **`serialID`**: Unique serial identifier for the product.
- **`productStatus`**: Status of the product (e.g., original, refurbished).

#### **Circularity**
- **`dismantlingAndRemovalInformation`**: List of documents related to dismantling and removal of the product, including document type, MIME type, and resource path.
- **`recycledContent`**: List containing information on pre-consumer and post-consumer recycled material shares, type of recycled material, and associated URLs.
- **`endOfLifeInformation`**: URLs and information about waste prevention, separate collection, and collection points for the product at the end of its life cycle.
- **`supplierInformation`**: Information about suppliers, including name, address, email, and website.

#### **Carbon Footprint**
- **`carbonFootprintPerLifecycleStage`**: List of lifecycle stages with associated carbon footprints (e.g., rawMaterial, production).
- **`carbonFootprintStudy`**: URL linking to the study or resource providing carbon footprint details.
- **`productCarbonFootprint`**: Total carbon footprint value of the product.
- **`carbonFootprintPerformanceClass`**: Classification label for the product's carbon footprint performance (e.g., "Carbon Trust label").

## **Contributing**

If you want to contribute to the `NMIS_Ecopass`, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
