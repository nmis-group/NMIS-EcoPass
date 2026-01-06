"""
Exporter Factory for creating output format exporters.
"""

from typing import Dict, Type, Any
from .base import BaseExporter
from .jsonld import JSONLDExporter


class ExporterFactory:
    """Factory for creating exporters."""
    
    _exporters: Dict[str, Type] = {
        'jsonld': JSONLDExporter,
        'json-ld': JSONLDExporter,
    }
    
    @classmethod
    def create(cls, exporter_type: str, **kwargs: Any):
        """
        Create an exporter instance.
        
        Args:
            exporter_type: Type of exporter ('jsonld')
            **kwargs: Arguments to pass to exporter constructor
            
        Returns:
            Configured exporter instance
        """
        exporter_type = exporter_type.lower()
        
        if exporter_type not in cls._exporters:
            available = ', '.join(cls._exporters.keys())
            raise ValueError(
                f"Unknown exporter type: '{exporter_type}'. "
                f"Available: {available}"
            )
        
        return cls._exporters[exporter_type](**kwargs)
    
    @classmethod
    def register(cls, name: str, exporter_class: Type) -> None:
        """Register a new exporter type."""
        cls._exporters[name.lower()] = exporter_class
    
    @classmethod
    def list_exporters(cls) -> list:
        """List available exporter types."""
        return list(set(cls._exporters.keys()))
