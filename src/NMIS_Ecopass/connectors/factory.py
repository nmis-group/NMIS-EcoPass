"""
Connector Factory for creating data source connectors.

Provides a factory pattern to instantiate connectors by name.
"""

from typing import Dict, Type, Any
from .base import BaseConnector
from .isa95 import ISA95Connector
from .csv_connector import CSVConnector
from .excel_connector import ExcelConnector


class ConnectorFactory:
    """Factory for creating data connectors."""
    
    _connectors: Dict[str, Type[BaseConnector]] = {
        'isa95': ISA95Connector,
        'csv': CSVConnector,
        'excel': ExcelConnector,
    }
    
    @classmethod
    def create(cls, connector_type: str, **kwargs: Any) -> BaseConnector:
        """
        Create a connector instance.
        
        Args:
            connector_type: Type of connector ('isa95', 'csv', 'excel')
            **kwargs: Arguments to pass to connector constructor
            
        Returns:
            Configured connector instance
            
        Raises:
            ValueError: If connector type is unknown
        """
        connector_type = connector_type.lower()
        
        if connector_type not in cls._connectors:
            available = ', '.join(cls._connectors.keys())
            raise ValueError(
                f"Unknown connector type: '{connector_type}'. "
                f"Available: {available}"
            )
        
        return cls._connectors[connector_type](**kwargs)
    
    @classmethod
    def register(cls, name: str, connector_class: Type[BaseConnector]) -> None:
        """Register a new connector type."""
        cls._connectors[name.lower()] = connector_class
    
    @classmethod
    def list_connectors(cls) -> list:
        """List available connector types."""
        return list(cls._connectors.keys())
