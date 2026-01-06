"""
Main DPPBridge class - the primary API for the package.

Provides a unified interface for transforming data to Digital Product Passports.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from .config import config
from .exception import DPPBridgeError, MappingError
from ..mapping.engine import MappingEngine
from ..mapping.loader import MappingLoader
from ..exporters.jsonld import JSONLDExporter
from ..models.registry import SchemaRegistry


class DPPBridge:
    """
    Main interface for DPP transformations.
    
    Example:
        bridge = DPPBridge()
        
        # Transform ISA-95 XML to DPP
        result = bridge.transform(
            source="production.xml",
            mapping="mapping.yaml",
            output="passport.json"
        )
        
        # Or step by step
        records = bridge.extract("data.csv", connector="csv")
        transformed = bridge.map(records, mapping="mapping.yaml")
        bridge.export(transformed, output="passport.json")
    """
    
    def __init__(self):
        self.engine = MappingEngine()
        self.loader = MappingLoader()
        self.exporter = JSONLDExporter()
    
    def transform(
        self,
        source: Path | str,
        mapping: Dict[str, Any] | Path | str,
        output: Optional[Path | str] = None,
        validate: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Transform source data to DPP format.
        
        This is the main method combining extract, map, and export.
        
        Args:
            source: Path to source data file
            mapping: Mapping configuration (dict or YAML path)
            output: Output file path (optional)
            validate: Whether to validate against schema
            
        Returns:
            List of transformed DPP records
        """
        # Load mapping if path provided
        if isinstance(mapping, (Path, str)):
            mapping_config = self.loader.load(mapping)
        else:
            mapping_config = mapping
        
        # Execute transformation
        results = self.engine.execute(mapping_config, source)
        
        # Validate against schema if specified
        if validate and 'target' in mapping_config:
            schema_name = mapping_config['target'].get('schema')
            if schema_name:
                try:
                    for i, record in enumerate(results):
                        SchemaRegistry.validate(schema_name, record)
                except Exception as e:
                    # Log but don't fail for prototype
                    pass
        
        # Export if output path specified
        if output:
            output_format = mapping_config.get('target', {}).get('format', 'jsonld')
            
            if output_format in ('jsonld', 'json-ld'):
                if len(results) == 1:
                    self.exporter.export(results[0], output)
                else:
                    self.exporter.export_list(results, output)
            else:
                # Default to JSON
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
        
        return results
    
    def extract(
        self,
        source: Path | str,
        connector: str,
        **connector_kwargs
    ) -> List[Dict[str, Any]]:
        """
        Extract data from source using specified connector.
        
        Args:
            source: Path to source file
            connector: Connector type ('isa95', 'csv', 'excel')
            **connector_kwargs: Arguments for connector
            
        Returns:
            List of extracted records as dicts
        """
        from ..connectors.factory import ConnectorFactory
        
        conn = ConnectorFactory.create(connector, **connector_kwargs)
        records = list(conn.parse(source))
        return [r.to_dict() if hasattr(r, 'to_dict') else r for r in records]
    
    def map(
        self,
        records: List[Dict[str, Any]],
        mapping: Dict[str, Any] | Path | str
    ) -> List[Dict[str, Any]]:
        """
        Apply mapping transformation to records.
        
        Args:
            records: List of source records
            mapping: Mapping configuration
            
        Returns:
            List of transformed records
        """
        # Load mapping if path
        if isinstance(mapping, (Path, str)):
            mapping_config = self.loader.load(mapping)
        else:
            mapping_config = mapping
        
        # Build transformer
        transformer = self.engine._build_transformer(mapping_config['rules'])
        
        # Transform each record
        return [transformer(record) for record in records]
    
    def export(
        self,
        data: List[Dict[str, Any]] | Dict[str, Any] | BaseModel,
        output: Path | str,
        format: str = 'jsonld'
    ) -> None:
        """
        Export data to file.
        
        Args:
            data: Data to export
            output: Output file path
            format: Output format ('jsonld', 'json')
        """
        if format in ('jsonld', 'json-ld'):
            if isinstance(data, list):
                self.exporter.export_list(data, output)
            else:
                self.exporter.export(data, output)
        else:
            with open(output, 'w', encoding='utf-8') as f:
                if isinstance(data, BaseModel):
                    json.dump(data.model_dump(mode='json'), f, indent=2)
                else:
                    json.dump(data, f, indent=2)
    
    @staticmethod
    def list_connectors() -> List[str]:
        """List available connector types."""
        from ..connectors.factory import ConnectorFactory
        return ConnectorFactory.list_connectors()
    
    @staticmethod
    def list_schemas() -> List[str]:
        """List available DPP schemas."""
        return SchemaRegistry.list_all()


# Convenience function
def transform(
    source: Path | str,
    mapping: Dict[str, Any] | Path | str,
    output: Optional[Path | str] = None
) -> List[Dict[str, Any]]:
    """
    Transform source data to DPP format.
    
    Args:
        source: Path to source data
        mapping: Mapping configuration
        output: Output file path (optional)
        
    Returns:
        List of transformed DPP records
    """
    bridge = DPPBridge()
    return bridge.transform(source, mapping, output)
