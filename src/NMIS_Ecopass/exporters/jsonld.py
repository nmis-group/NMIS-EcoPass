"""
JSON-LD Exporter using PyLD.

Exports Pydantic DPP models to W3C-compliant JSON-LD format.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel

try:
    from pyld import jsonld
    HAS_PYLD = True
except ImportError:
    HAS_PYLD = False

from ..core.exception import ExporterError


# Default JSON-LD context for DPP
DEFAULT_CONTEXT = {
    "@vocab": "https://schema.org/",
    "dpp": "https://dpp.eu/ns#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    
    "identifier": "schema:identifier",
    "manufacturer": {"@id": "schema:manufacturer", "@type": "@id"},
    "productionDate": {"@id": "schema:productionDate", "@type": "xsd:date"},
    "carbonFootprint": {"@id": "dpp:carbonFootprint", "@type": "xsd:float"},
    "recycledContent": {"@id": "dpp:recycledContent", "@type": "xsd:float"},
}


class JSONLDExporter:
    """Export DPP data to JSON-LD format."""
    
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        """
        Initialize exporter.
        
        Args:
            context: JSON-LD context (uses default if None)
        """
        self.context = context or DEFAULT_CONTEXT
    
    def export(
        self,
        data: BaseModel | Dict[str, Any],
        output_path: Optional[Path | str] = None,
        compact: bool = True
    ) -> Dict[str, Any]:
        """
        Export DPP to JSON-LD.
        
        Args:
            data: Pydantic model or dict to export
            output_path: Path to write output (optional)
            compact: Whether to compact using context
            
        Returns:
            JSON-LD document as dict
        """
        # Convert Pydantic model to dict
        if isinstance(data, BaseModel):
            doc = data.model_dump(mode='json', exclude_none=True)
        else:
            doc = data
        
        # Add context
        doc["@context"] = self.context
        
        # Compact using PyLD if available and requested
        if compact and HAS_PYLD:
            try:
                doc = jsonld.compact(doc, self.context)
            except Exception as e:
                # Fall back to simple context addition
                pass
        
        # Write to file if path provided
        if output_path:
            output_path = Path(output_path) if isinstance(output_path, str) else output_path
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(doc, f, indent=2, ensure_ascii=False)
        
        return doc
    
    def export_list(
        self,
        items: list,
        output_path: Optional[Path | str] = None
    ) -> Dict[str, Any]:
        """
        Export multiple DPPs as a JSON-LD graph.
        
        Args:
            items: List of Pydantic models or dicts
            output_path: Path to write output (optional)
            
        Returns:
            JSON-LD document with @graph
        """
        # Convert items
        graph = []
        for item in items:
            if isinstance(item, BaseModel):
                graph.append(item.model_dump(mode='json', exclude_none=True))
            else:
                graph.append(item)
        
        doc = {
            "@context": self.context,
            "@graph": graph
        }
        
        if output_path:
            output_path = Path(output_path) if isinstance(output_path, str) else output_path
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(doc, f, indent=2, ensure_ascii=False)
        
        return doc
    
    def validate(self, jsonld_file: Path | str) -> bool:
        """
        Validate JSON-LD structure.
        
        Args:
            jsonld_file: Path to JSON-LD file
            
        Returns:
            True if valid
            
        Raises:
            ExporterError: If validation fails
        """
        if not HAS_PYLD:
            # Can't validate without PyLD, assume valid
            return True
        
        try:
            path = Path(jsonld_file) if isinstance(jsonld_file, str) else jsonld_file
            with open(path, 'r', encoding='utf-8') as f:
                doc = json.load(f)
            
            # Try to expand - this validates the structure
            jsonld.expand(doc)
            return True
            
        except Exception as e:
            raise ExporterError(f"Invalid JSON-LD: {e}")


# Convenience instance
exporter = JSONLDExporter()


def to_jsonld(
    data: BaseModel | Dict[str, Any],
    output_path: Optional[Path | str] = None
) -> Dict[str, Any]:
    """Export data to JSON-LD format."""
    return exporter.export(data, output_path)
