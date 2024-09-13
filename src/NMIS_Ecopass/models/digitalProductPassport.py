from pydantic import BaseModel
from typing import Optional
from .metadata import Metadata
from .productIdentifier import ProductIdentifier
from .carbonFootprint import CarbonFootprint
from . circularity import Circularity

class DigitalProductPassport(BaseModel):
    metadata: Optional[Metadata] = None
    productIdentifer:Optional[ProductIdentifier] = None
    circularity:Optional[Circularity] = None
    carbonFootprint:Optional[CarbonFootprint] = None


