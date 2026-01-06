"""
YAML Mapping Loader with Yamale validation.

Loads and validates mapping configuration files against the schema.
"""

import yaml
import yamale
from pathlib import Path
from typing import Dict, Any, Optional
from ..core.exception import MappingError


class MappingLoader:
    """Load and validate mapping YAML files."""
    
    def __init__(self, schema_path: Optional[Path] = None):
        """
        Initialize loader with schema.
        
        Args:
            schema_path: Path to Yamale schema (uses default if None)
        """
        if schema_path is None:
            schema_path = Path(__file__).parent / "mapping_schema.yaml"
        
        self.schema_path = schema_path
        self._schema = None
    
    @property
    def schema(self):
        """Lazy load the Yamale schema."""
        if self._schema is None:
            self._schema = yamale.make_schema(str(self.schema_path))
        return self._schema
    
    def load(self, mapping_file: Path | str) -> Dict[str, Any]:
        """
        Load and validate a mapping file.
        
        Args:
            mapping_file: Path to YAML mapping file
            
        Returns:
            Validated mapping dictionary
            
        Raises:
            MappingError: If validation fails
        """
        mapping_path = Path(mapping_file) if isinstance(mapping_file, str) else mapping_file
        
        if not mapping_path.exists():
            raise MappingError(f"Mapping file not found: {mapping_path}")
        
        try:
            # Load and validate with Yamale
            data = yamale.make_data(str(mapping_path))
            yamale.validate(self.schema, data)
            
            # Return the actual content (Yamale returns list of tuples)
            return data[0][0]
            
        except yamale.YamaleError as e:
            # Format validation errors nicely
            errors = []
            for result in e.results:
                for error in result.errors:
                    errors.append(f"  - {error}")
            
            raise MappingError(
                f"Invalid mapping file '{mapping_path.name}':\n" + 
                "\n".join(errors)
            )
        except yaml.YAMLError as e:
            raise MappingError(f"YAML syntax error in {mapping_path.name}: {e}")
    
    def load_raw(self, mapping_file: Path | str) -> Dict[str, Any]:
        """
        Load a mapping file without schema validation.
        
        Useful for debugging or partial mappings.
        
        Args:
            mapping_file: Path to YAML mapping file
            
        Returns:
            Raw mapping dictionary
        """
        mapping_path = Path(mapping_file) if isinstance(mapping_file, str) else mapping_file
        
        with open(mapping_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
