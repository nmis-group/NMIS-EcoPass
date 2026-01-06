from abc import ABC, abstractmethod
from typing import Iterator, Any, Dict
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class DataRecord:
    """
    Flat representation of parsed data with path-based access.
    
    Stores data as flattened paths for easy mapping.
    Example: {"MaterialLot/ID": "BAT-001", "MaterialLot/Property[@ID='capacity']/Value": "100"}
    """
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __getitem__(self, key: str) -> Any:
        """Get value by key"""
        return self.data.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set value by key"""
        self.data[key] = value
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get value using path notation.
        
        Args:
            path: Dot-separated path (e.g., 'MaterialLot/ID')
            default: Default value if not found
            
        Returns:
            Value at path or default
        """
        return self.data.get(path, default)
    
    def items(self):
        """Iterate over key-value pairs"""
        return self.data.items()
    
    def keys(self):
        """Get all keys"""
        return self.data.keys()
    
    def values(self):
        """Get all values"""
        return self.data.values()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.data.copy()


class BaseConnector(ABC):
    """
    Abstract base class for data source connectors.
    
    All connectors must implement the parse method to convert
    source data into DataRecord objects.
    """
    
    @abstractmethod
    def parse(self, source: Path | str | bytes) -> Iterator[DataRecord]:
        """
        Parse source data and yield DataRecord objects.
        
        Args:
            source: Path to file, string content, or bytes
            
        Yields:
            DataRecord objects
            
        Raises:
            ConnectorError: If parsing fails
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Describe the structure of data this connector produces.
        
        Returns:
            Dictionary describing available fields and types
        """
        return {
            "connector": self.__class__.__name__,
            "description": self.__doc__,
        }