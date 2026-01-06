# Provide helpful error messages for the user

class DPPBridgeError(Exception):
    """Base exception for DPP Bridge"""
    pass

class SchemaNotFoundError(DPPBridgeError):
    """Raised when schema is not registered"""
    pass

class ConnectorError(DPPBridgeError):
    """Raised when connector fails to parse"""
    pass

class MappingError(DPPBridgeError):
    """Raised when mapping transformation fails"""
    pass

class ValidationError(DPPBridgeError):
    """Raised when DPP validation fails"""
    pass

class ExporterError(DPPBridgeError):
    """Raised when export fails"""
    pass