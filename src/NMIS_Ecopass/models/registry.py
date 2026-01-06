"""
Schema Registry for DPP models.

Central registry for schema classes and their JSON-LD contexts.
"""

from typing import Dict, Type, Any, Optional
from pydantic import BaseModel

from ..core.exception import SchemaNotFoundError


class SchemaRegistry:
    """Registry for DPP schemas and contexts."""
    
    _schemas: Dict[str, Type[BaseModel]] = {}
    _contexts: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register(
        cls,
        name: str,
        schema_class: Type[BaseModel],
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a schema.
        
        Args:
            name: Schema name (e.g., 'battery_passport')
            schema_class: Pydantic model class
            context: JSON-LD context for this schema
        """
        cls._schemas[name.lower()] = schema_class
        if context:
            cls._contexts[name.lower()] = context
    
    @classmethod
    def get_schema(cls, name: str) -> Type[BaseModel]:
        """
        Get a registered schema class.
        
        Args:
            name: Schema name
            
        Returns:
            Pydantic model class
            
        Raises:
            SchemaNotFoundError: If schema not registered
        """
        name = name.lower()
        if name not in cls._schemas:
            available = ', '.join(cls._schemas.keys()) or '(none)'
            raise SchemaNotFoundError(
                f"Schema '{name}' not found. Available: {available}"
            )
        return cls._schemas[name]
    
    @classmethod
    def get_context(cls, name: str) -> Dict[str, Any]:
        """
        Get JSON-LD context for a schema.
        
        Args:
            name: Schema name
            
        Returns:
            JSON-LD context dict
        """
        return cls._contexts.get(name.lower(), {})
    
    @classmethod
    def list_all(cls) -> list:
        """List all registered schema names."""
        return list(cls._schemas.keys())
    
    @classmethod
    def validate(cls, name: str, data: Dict[str, Any]) -> BaseModel:
        """
        Validate data against a schema.
        
        Args:
            name: Schema name
            data: Data dict to validate
            
        Returns:
            Validated Pydantic model instance
        """
        schema = cls.get_schema(name)
        return schema.model_validate(data)


def _auto_register_schemas():
    """Auto-register available DPP schemas."""
    try:
        from ..models.ReMakeDPP.digitalProductPassport import DigitalProductPassport
        SchemaRegistry.register('dpp', DigitalProductPassport)
        SchemaRegistry.register('digital_product_passport', DigitalProductPassport)
    except ImportError:
        pass
    
    try:
        from ..models.BatteryPass import BatteryPassport
        SchemaRegistry.register('battery_passport', BatteryPassport)
        SchemaRegistry.register('battery_pass', BatteryPassport)
    except ImportError:
        pass


# Auto-register on import
_auto_register_schemas()
