from .metadata import Metadata
from .circularity import Circularity
from .productIdentifier import ProductIdentifier
from .digitalProductPassport import DigitalProductPassport as DPP
from .carbonFootprint import CarbonFootprint
from .remanufacture import RepairModel
from .materialComposition import MaterialInformation
from .additionalData import AdditionalData

__all__ = [
    "Metadata",
    "Circularity",
    "ProductIdentifier",
    "DPP",
    "CarbonFootprint",
    "RepairModel",
    "MaterialInformation",
    "AdditionalData"
    
]