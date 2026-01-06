"""
Bonobo-based Mapping Engine for DPP transformations.

Executes data transformations using Bonobo ETL graphs.
"""

try:
    import bonobo
    HAS_BONOBO = True
except ImportError:
    HAS_BONOBO = False

from typing import Dict, Any, Iterator, Callable, List
from pathlib import Path

from .loader import MappingLoader
from .transforms import TransformRegistry
from ..connectors.factory import ConnectorFactory
from ..connectors.base import DataRecord
from ..core.exception import MappingError


class MappingEngine:
    """Execute data transformations using Bonobo graphs."""
    
    def __init__(self):
        self.transforms = TransformRegistry()
        self.loader = MappingLoader()
    
    def execute(
        self, 
        mapping: Dict[str, Any] | Path | str,
        source_file: Path | str
    ) -> List[Dict[str, Any]]:
        """
        Execute mapping transformation.
        
        Args:
            mapping: Mapping dict or path to YAML file
            source_file: Path to source data file
            
        Returns:
            List of transformed records
        """
        # Load mapping if path provided
        if isinstance(mapping, (Path, str)):
            mapping = self.loader.load(mapping)
        
        # Get mapping metadata and rules
        mapping_meta = mapping['mapping'] if 'mapping' in mapping else mapping
        rules = mapping['rules'] if 'rules' in mapping else []
        
        # Get connector
        source_config = mapping_meta['source']
        connector_type = source_config['connector']
        connector_kwargs = {}
        if 'root' in source_config:
            connector_kwargs['root_element'] = source_config['root']
        
        connector = ConnectorFactory.create(connector_type, **connector_kwargs)
        
        # Parse source data
        records = list(connector.parse(source_file))
        
        # Build transformer
        transformer = self._build_transformer(rules)
        
        # Transform records
        results = []
        for record in records:
            try:
                transformed = transformer(record)
                results.append(transformed)
            except Exception as e:
                raise MappingError(f"Transformation failed: {e}")
        
        return results
    
    def execute_bonobo(
        self, 
        mapping: Dict[str, Any] | Path | str,
        source_file: Path | str
    ) -> List[Dict[str, Any]]:
        """
        Execute using Bonobo graph (for parallel processing).
        
        Args:
            mapping: Mapping dict or path to YAML file
            source_file: Path to source data file
            
        Returns:
            List of transformed records
        """
        if not HAS_BONOBO:
            raise MappingError("Bonobo not installed. Parallel execution unavailable.")
            
        # Load mapping if path provided
        if isinstance(mapping, (Path, str)):
            mapping = self.loader.load(mapping)
        
        # Get mapping metadata
        mapping_meta = mapping['mapping'] if 'mapping' in mapping else mapping
        rules = mapping['rules'] if 'rules' in mapping else []
        
        # Collect results
        results = []
        
        def collect(record):
            results.append(record)
        
        # Build graph
        graph = bonobo.Graph(
            self._make_extractor(mapping_meta, source_file),
            self._build_transformer(rules),
            collect
        )
        
        # Execute
        bonobo.run(graph)
        
        return results
    
    def _make_extractor(
        self, 
        mapping_meta: Dict[str, Any], 
        source_file: Path | str
    ) -> Callable:
        """Create an extraction function for Bonobo."""
        source_config = mapping_meta['source']
        connector_type = source_config['connector']
        connector_kwargs = {}
        if 'root' in source_config:
            connector_kwargs['root_element'] = source_config['root']
        
        connector = ConnectorFactory.create(connector_type, **connector_kwargs)
        
        def extract():
            for record in connector.parse(source_file):
                yield record.to_dict() if hasattr(record, 'to_dict') else record
        
        return extract
    
    def _build_transformer(self, rules: List[Dict]) -> Callable:
        """
        Build transformation function from rules.
        
        Args:
            rules: List of mapping rules
            
        Returns:
            Transformation function
        """
        transforms = self.transforms
        
        def transform(record: Dict[str, Any] | DataRecord) -> Dict[str, Any]:
            # Convert DataRecord to dict if needed
            if isinstance(record, DataRecord):
                record = record.to_dict()
            
            result = {}
            
            for rule in rules:
                source_path = rule['source']
                target_path = rule['target']
                
                # Get value from source
                value = record.get(source_path)
                
                # Handle required fields
                if value is None:
                    if rule.get('required', False):
                        raise MappingError(
                            f"Required field missing: {source_path}"
                        )
                    value = rule.get('default')
                
                # Apply transform if specified
                if value is not None and 'transform' in rule:
                    transform_config = rule['transform']
                    value = transforms.apply(value, transform_config)
                
                # Set value in result using dot notation
                if value is not None:
                    _set_nested(result, target_path, value)
            
            return result
        
        return transform


def _set_nested(data: Dict, path: str, value: Any) -> None:
    """
    Set nested value using dot notation.
    
    Example:
        data = {}
        _set_nested(data, "performance.rated_capacity_ah", 100.5)
        # data = {"performance": {"rated_capacity_ah": 100.5}}
    """
    keys = path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value


# Convenience function
def transform(
    source_file: Path | str,
    mapping: Dict[str, Any] | Path | str
) -> List[Dict[str, Any]]:
    """
    Transform source data using mapping configuration.
    
    Args:
        source_file: Path to source data
        mapping: Mapping dict or path to YAML
        
    Returns:
        List of transformed records
    """
    engine = MappingEngine()
    return engine.execute(mapping, source_file)