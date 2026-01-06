"""
NMIS EcoPass - Digital Product Passport ETL Package

Transform manufacturing data (ISA-95, CSV, Excel) into
EU-compliant Digital Product Passports (JSON-LD format).

Example:
    from NMIS_Ecopass import DPPBridge
    
    bridge = DPPBridge()
    result = bridge.transform(
        source="production.xml",
        mapping="mapping.yaml",
        output="passport.json"
    )
"""

__version__ = "0.2.0"

# Main API
from .core.bridge import DPPBridge, transform

# Connectors
from .connectors.factory import ConnectorFactory
from .connectors.base import BaseConnector, DataRecord
from .connectors.isa95 import ISA95Connector
from .connectors.csv_connector import CSVConnector
from .connectors.excel_connector import ExcelConnector

# Mapping
from .mapping.engine import MappingEngine
from .mapping.loader import MappingLoader
from .mapping.transforms import TransformRegistry

# Exporters
from .exporters.jsonld import JSONLDExporter, to_jsonld
from .exporters.factory import ExporterFactory

# Models
from .models.registry import SchemaRegistry

# Exceptions
from .core.exception import (
    DPPBridgeError,
    ConnectorError,
    MappingError,
    ValidationError,
    ExporterError,
    SchemaNotFoundError,
)

__all__ = [
    # Version
    "__version__",
    # Main
    "DPPBridge",
    "transform",
    # Connectors
    "ConnectorFactory",
    "BaseConnector",
    "DataRecord",
    "ISA95Connector",
    "CSVConnector",
    "ExcelConnector",
    # Mapping
    "MappingEngine",
    "MappingLoader",
    "TransformRegistry",
    # Exporters
    "JSONLDExporter",
    "ExporterFactory",
    "to_jsonld",
    # Models
    "SchemaRegistry",
    # Exceptions
    "DPPBridgeError",
    "ConnectorError",
    "MappingError",
    "ValidationError",
    "ExporterError",
    "SchemaNotFoundError",
]
