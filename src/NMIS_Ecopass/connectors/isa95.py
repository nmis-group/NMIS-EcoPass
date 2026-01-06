from pathlib import Path
from typing import Iterator, List
from xml.etree import ElementTree as ET
from .base import BaseConnector, DataRecord
from ..core.exception import ConnectorError

# Standard B2MML namespace
B2MML_NS = "http://www.mesa.org/xml/B2MML"


class ISA95Connector(BaseConnector):
    """
    Connector for ISA-95 B2MML XML files.
    
    Parses common B2MML elements:
    - MaterialLot: Production batches
    - ProductionResponse: Completed work
    - SegmentResponse: Process steps
    
    Example:
        connector = ISA95Connector()
        for record in connector.parse("production_data.xml"):
            batch_id = record.get("MaterialLot/ID")
            capacity = record.get("MaterialLot/Property[@ID='capacity']/Value")
    """
    
    def __init__(self, root_element: str = "MaterialLot"):
        """
        Initialize ISA-95 connector.
        
        Args:
            root_element: XML element to extract as records
                         (MaterialLot, ProductionResponse, etc.)
        """
        self.root_element = root_element
        self.namespace = B2MML_NS
    
    def parse(self, source: Path | str | bytes) -> Iterator[DataRecord]:
        """
        Parse B2MML XML and yield flat data records.
        
        Args:
            source: Path to XML file, XML string, or XML bytes
            
        Yields:
            DataRecord objects with flattened paths
            
        Raises:
            ConnectorError: If XML parsing fails
        """
        try:
            # Load XML
            if isinstance(source, bytes):
                root = ET.fromstring(source)
            elif isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
                tree = ET.parse(source)
                root = tree.getroot()
            else:
                # Assume XML string
                root = ET.fromstring(source)
            
            # Detect namespace from root element
            if root.tag.startswith('{'):
                self.namespace = root.tag[1:root.tag.index('}')]
            
            # Find target elements
            elements = self._find_elements(root, self.root_element)
            
            if not elements:
                raise ConnectorError(
                    f"No '{self.root_element}' elements found in XML"
                )
            
            # Convert each element to a record
            for element in elements:
                yield self._to_record(element)
                
        except ET.ParseError as e:
            raise ConnectorError(f"Failed to parse XML: {e}")
        except Exception as e:
            raise ConnectorError(f"Unexpected error parsing ISA-95: {e}")
    
    def _find_elements(self, root: ET.Element, tag: str) -> List[ET.Element]:
        """
        Find elements handling namespaces automatically.
        
        Args:
            root: Root XML element
            tag: Element tag to find
            
        Returns:
            List of matching elements
        """
        # Try with namespace
        results = root.findall(f".//{{{self.namespace}}}{tag}")
        
        # Fallback without namespace
        if not results:
            results = root.findall(f".//{tag}")
        
        return results
    
    def _to_record(self, element: ET.Element, prefix: str = "") -> DataRecord:
        """
        Convert XML element to flat DataRecord.
        
        Args:
            element: XML element
            prefix: Path prefix for nested elements
            
        Returns:
            DataRecord with flattened paths
        """
        record = DataRecord()
        self._parse_recursive(element, record, prefix)
        return record
    
    def _parse_recursive(
        self, 
        elem: ET.Element, 
        record: DataRecord, 
        prefix: str
    ) -> None:
        """
        Recursively parse element into flat key-value pairs.
        
        Creates paths like:
        - MaterialLot/ID
        - MaterialLot/Property[@ID='capacity']/Value
        - SegmentResponse/ActualStartTime
        
        Args:
            elem: Current XML element
            record: DataRecord to populate
            prefix: Current path prefix
        """
        # Get local tag (strip namespace)
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        path = f"{prefix}/{tag}" if prefix else tag
        
        # Store text content if present
        if elem.text and elem.text.strip():
            record[path] = elem.text.strip()
        
        # Store attributes
        for attr, value in elem.attrib.items():
            if not attr.startswith('{'):  # Skip namespace attributes
                record[f"{path}/@{attr}"] = value
        
        # Process children
        for child in elem:
            self._parse_recursive(child, record, path)
        
        # Special handling for Property elements (common B2MML pattern)
        # Allows access like: Property[@ID='capacity']/Value
        if tag == "Property":
            prop_id = record.get(f"{path}/ID")
            prop_value = record.get(f"{path}/Value")
            
            if prop_id and prop_value:
                parent = prefix if prefix else ""
                # Create XPath-like access pattern
                record[f"{parent}/Property[@ID='{prop_id}']/Value"] = prop_value
    
    def get_schema(self) -> dict:
        """Describe ISA-95 connector output structure"""
        return {
            "connector": "ISA95Connector",
            "description": "ISA-95 B2MML XML Parser",
            "root_element": self.root_element,
            "namespace": self.namespace,
            "common_paths": [
                "MaterialLot/ID",
                "MaterialLot/MaterialDefinitionID",
                "MaterialLot/Property[@ID='...']/Value",
                "SegmentResponse/ActualStartTime",
                "SegmentResponse/EquipmentActual/EquipmentID",
                "ProductionResponse/ID"
            ]
        }