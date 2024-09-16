from pydantic import BaseModel,Field
from typing import Optional
from .metadata import Metadata
from .productIdentifier import ProductIdentifier
from .carbonFootprint import CarbonFootprint
from . circularity import Circularity

class DigitalProductPassport(BaseModel):
    metadata: Optional[Metadata] = Field(default_factory=Metadata)
    productIdentifier: Optional[ProductIdentifier] = Field(default_factory=ProductIdentifier)
    circularity: Optional[Circularity] = Field(default_factory=Circularity)
    carbonFootprint: Optional[CarbonFootprint] = Field(default_factory=CarbonFootprint)


