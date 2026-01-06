"""
Base exporter protocol.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel


class BaseExporter(ABC):
    """Abstract base class for data exporters."""
    
    @abstractmethod
    def export(
        self,
        data: BaseModel | Dict[str, Any],
        output_path: Optional[Path | str] = None
    ) -> Any:
        """
        Export data to target format.
        
        Args:
            data: Data to export
            output_path: Path to write output (optional)
            
        Returns:
            Exported data
        """
        pass
