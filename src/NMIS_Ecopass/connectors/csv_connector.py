import csv
from pathlib import Path
from typing import Iterator
from .base import BaseConnector, DataRecord
from ..core.exception import ConnectorError
from ..core.config import config


class CSVConnector(BaseConnector):
    """
    Connector for CSV files.
    
    Features:
    - Automatic delimiter detection
    - Header whitespace stripping
    - Multiple encoding support
    
    Example:
        connector = CSVConnector()
        for record in connector.parse("products.csv"):
            product_id = record.get("product_id")
            name = record.get("product_name")
    """
    
    def __init__(
        self,
        delimiter: str = None,
        encoding: str = None,
        skip_rows: int = 0
    ):
        """
        Initialize CSV connector.
        
        Args:
            delimiter: Column delimiter (auto-detect if None)
            encoding: File encoding (default from config)
            skip_rows: Number of rows to skip before header
        """
        self.delimiter = delimiter or config.csv_delimiter
        self.encoding = encoding or config.csv_encoding
        self.skip_rows = skip_rows
    
    def parse(self, source: Path | str) -> Iterator[DataRecord]:
        """
        Parse CSV file and yield records.
        
        Args:
            source: Path to CSV file
            
        Yields:
            DataRecord objects (one per row)
            
        Raises:
            ConnectorError: If CSV parsing fails
        """
        try:
            source_path = Path(source) if isinstance(source, str) else source
            
            with open(source_path, 'r', encoding=self.encoding, newline='') as f:
                # Skip rows if specified
                for _ in range(self.skip_rows):
                    next(f)
                
                # Auto-detect delimiter if needed
                if self.delimiter == ",":
                    sample = f.read(4096)
                    f.seek(0)
                    sniffer = csv.Sniffer()
                    try:
                        self.delimiter = sniffer.sniff(sample).delimiter
                    except csv.Error:
                        pass  # Use default delimiter
                
                reader = csv.DictReader(f, delimiter=self.delimiter)
                
                for row in reader:
                    # Strip whitespace from keys and values
                    clean_row = {
                        k.strip(): v.strip() if isinstance(v, str) else v
                        for k, v in row.items()
                    }
                    yield DataRecord(data=clean_row)
                    
        except FileNotFoundError:
            raise ConnectorError(f"CSV file not found: {source}")
        except Exception as e:
            raise ConnectorError(f"Failed to parse CSV: {e}")
    
    def get_schema(self) -> dict:
        """Describe CSV connector output"""
        return {
            "connector": "CSVConnector",
            "description": "CSV File Parser",
            "delimiter": self.delimiter,
            "encoding": self.encoding
        }