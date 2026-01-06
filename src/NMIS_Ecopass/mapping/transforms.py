"""
Transform registry with built-in transformation functions.

Provides type conversions, lookups, templates, and aggregations.
"""

from typing import Any, Dict, Callable, Optional
from datetime import datetime
from dateutil import parser as dateparser


class TransformRegistry:
    """Registry of available transform functions."""
    
    def __init__(self):
        self._transforms: Dict[str, Callable] = {}
        self._register_builtin()
    
    def _register_builtin(self):
        """Register built-in transforms."""
        self.register('str', self._to_str)
        self.register('int', self._to_int)
        self.register('float', self._to_float)
        self.register('datetime', self._to_datetime)
        self.register('lookup', self._lookup)
        self.register('template', self._template)
        self.register('aggregate', self._aggregate)
    
    def register(self, name: str, func: Callable) -> None:
        """Register a transform function."""
        self._transforms[name] = func
    
    def get(self, name: str) -> Callable:
        """Get a transform function by name."""
        if name not in self._transforms:
            available = ', '.join(self._transforms.keys())
            raise ValueError(f"Unknown transform: '{name}'. Available: {available}")
        return self._transforms[name]
    
    def apply(self, value: Any, transform_config: Dict[str, Any]) -> Any:
        """
        Apply a transform to a value.
        
        Args:
            value: Input value
            transform_config: Transform configuration with 'type' key
            
        Returns:
            Transformed value
        """
        transform_type = transform_config.get('type', 'str')
        transform_func = self.get(transform_type)
        return transform_func(value, **transform_config)
    
    @staticmethod
    def _to_str(value: Any, **kwargs) -> str:
        """Convert to string."""
        if value is None:
            return kwargs.get('default', '')
        return str(value)
    
    @staticmethod
    def _to_int(value: Any, **kwargs) -> Optional[int]:
        """Convert to integer."""
        if value is None or value == '':
            return kwargs.get('default')
        try:
            # Handle float strings like "123.45"
            return int(float(value))
        except (ValueError, TypeError):
            return kwargs.get('default')
    
    @staticmethod
    def _to_float(value: Any, precision: int = None, **kwargs) -> Optional[float]:
        """Convert to float with optional precision."""
        if value is None or value == '':
            return kwargs.get('default')
        try:
            result = float(value)
            if precision is not None:
                result = round(result, precision)
            return result
        except (ValueError, TypeError):
            return kwargs.get('default')
    
    @staticmethod
    def _to_datetime(
        value: str, 
        input_format: str = None, 
        output_format: str = None,
        **kwargs
    ) -> Optional[str]:
        """
        Parse and format datetime strings.
        
        Args:
            value: Input datetime string
            input_format: strptime format for parsing (auto-detect if None)
            output_format: strftime format for output (ISO if None)
            
        Returns:
            Formatted datetime string
        """
        if value is None or value == '':
            return kwargs.get('default')
        
        try:
            # Parse datetime
            if input_format:
                dt = datetime.strptime(value, input_format)
            else:
                dt = dateparser.parse(value)
            
            # Format output
            if output_format:
                return dt.strftime(output_format)
            return dt.isoformat()
            
        except (ValueError, TypeError):
            return kwargs.get('default')
    
    @staticmethod
    def _lookup(value: Any, table: Dict[str, Any] = None, **kwargs) -> Any:
        """
        Lookup value in a mapping table.
        
        Args:
            value: Key to look up
            table: Mapping dictionary
            
        Returns:
            Mapped value or default
        """
        if table is None:
            return kwargs.get('default')
        return table.get(str(value), kwargs.get('default'))
    
    @staticmethod
    def _template(value: Any = None, template: str = "", **kwargs) -> str:
        """
        Format string template with value.
        
        The template can use {value} placeholder.
        
        Args:
            value: Value to insert
            template: Format string
            
        Returns:
            Formatted string
        """
        try:
            return template.format(value=value, **kwargs)
        except (KeyError, ValueError):
            return template
    
    @staticmethod
    def _aggregate(values: list, operation: str = 'collect', **kwargs) -> Any:
        """
        Aggregate multiple values.
        
        Args:
            values: List of values to aggregate
            operation: 'sum', 'count', or 'collect'
            
        Returns:
            Aggregated result
        """
        if not isinstance(values, list):
            values = [values]
        
        if operation == 'sum':
            return sum(float(v) for v in values if v is not None)
        elif operation == 'count':
            return len([v for v in values if v is not None])
        elif operation == 'collect':
            return [v for v in values if v is not None]
        else:
            return values


# Global instance for convenience
transforms = TransformRegistry()
