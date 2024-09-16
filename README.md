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
    - [Step 2: Create a Metadata Instance](#step-2-create-a-metadata-instance)
    - [Step 3: Create a Circularity Instance](#step-3-create-a-circularity-instance)
    - [Step 4: Create the DPP Instance](#step-4-create-the-dpp-instance)
4. [Full Example](#full-example)
5. [Model Details](#model-details)
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

First, import the necessary classes from `DPP_framework`:

```python
from dpp_framework import DigitalProductPassport, Metadata, Circularity, ProductIdentifier, CarbonFootprint
from datetime import datetime
```

#### **Step 2: Create a Metadata Instance**

The `Metadata` model is a key component of the DPP. You can initialize it with required and optional fields:

```python
metadata_instance = Metadata(
    backup_reference="https://example.com/backup", # Optional - Any Third Party DPP platform as backup
    registration_identifier="https://example.com/registration/12345", # Unique DPP identifier
    economic_operator_id="ECO-987654321", #Company unique alphanumeric code
    last_modification=datetime.utcnow(), # Optional Data of DPP modification
    predecessor="https://example.com/registration/12344", # Optional - any predecessor DPP, eg. subassembly from supplier
    issue_date=datetime(2024, 1, 15, 9, 0, 0), #DPP issue date
    version="1.2.3", #DPP version not the product
    passport_identifier="123e4567-e89b-12d3-a456-426614174000", #Utilise UUID package to create identifier for each product passport
    status="active", #Enum - draft, active, inactive, expired
    expiration_date=datetime(2025, 1, 15, 9, 0, 0) #How long will this DPP will be valid
)
```

#### **Step 3: Create a Circularity Instance**

The `Circularity` model contains information about the product's lifecycle:

```python
circularity_instance = Circularity(
    renewable_content=25.0,
    # Other circularity fields...
)
```

#### **Step 4: Create the DPP Instance**

Finally, create a `DigitalProductPassport` instance and assign the models you've created:

```python
dpp_instance = DigitalProductPassport(
    metadata=metadata_instance,
    circularity=circularity_instance
    # Add other components like ProductIdentifier, CarbonFootprint as needed
)
```

You can now use `dpp_instance` to access the data in your DPP.

## **Full Example**

Here’s a full example that demonstrates creating a `DigitalProductPassport`:

```python
from dpp_framework import DigitalProductPassport, Metadata, Circularity, ProductIdentifier, CarbonFootprint
from datetime import datetime
from uuid import UUID

# Create Metadata instance
metadata_instance = Metadata(
    backup_reference="https://example.com/backup",
    registration_identifier="https://example.com/registration/12345",
    economic_operator_id="ECO-987654321",
    last_modification=datetime.utcnow(),
    predecessor="https://example.com/registration/12344",
    issue_date=datetime(2024, 1, 15, 9, 0, 0),
    version="1.2.3",
    passport_identifier=UUID("123e4567-e89b-12d3-a456-426614174000"),
    status="active",
    expiration_date=datetime(2025, 1, 15, 9, 0, 0)
)

# Create Circularity instance
circularity_instance = Circularity(
    renewable_content=25.0,
    # Additional circularity fields can be set here
)

# Create the DPP instance
dpp_instance = DigitalProductPassport(
    metadata=metadata_instance,
    circularity=circularity_instance
    # Add other components (e.g., ProductIdentifier, CarbonFootprint) if needed
)

# Access and modify fields
print(dpp_instance.metadata.economic_operator_id)
dpp_instance.metadata.version = "2.0.0"
```

## **Model Details**

### **Metadata**
- **`backup_reference`**: URL to a backup version of the DPP.
- **`registration_identifier`**: URL to the EU Registry.
- **`economic_operator_id`**: Identifier for the economic operator (e.g., tax code).
- **`last_modification`**: Timestamp of the last modification.
- **`predecessor`**: Reference to the previous version of the DPP.
- **`issue_date`**: Date when the DPP was issued.
- **`version`**: Internal version of the DPP.
- **`passport_identifier`**: Unique UUID4 for the passport.
- **`status`**: Status of the metadata (e.g., draft, active).
- **`expiration_date`**: Expiration date of the DPP.

### **Circularity**
- **`renewable_content`**: The percentage of renewable content in the product.
- **Additional Fields**: More fields can be added as per the circularity model's definition.

## **Contributing**

If you want to contribute to the `DPP_framework`, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
