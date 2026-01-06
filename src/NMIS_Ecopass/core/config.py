# Store package-level configuration
# Default settings for connectors/exporters
# Extensible for future config options

from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class DPPBridgeConfig:
    """Global configuration for DPP Bridge"""
    
    # Default paths
    library_path: Path = Path(__file__).parent.parent / "library"
    mappings_path: Optional[Path] = None
    
    # Connector defaults
    csv_delimiter: str = ","
    csv_encoding: str = "utf-8"
    xml_namespace_aware: bool = True
    
    # Exporter defaults
    jsonld_indent: int = 2
    jsonld_ensure_ascii: bool = False
    
    # Validation
    strict_validation: bool = True
    
    def __post_init__(self):
        if self.mappings_path is None:
            self.mappings_path = self.library_path / "mappings"

# Global config instance
config = DPPBridgeConfig()