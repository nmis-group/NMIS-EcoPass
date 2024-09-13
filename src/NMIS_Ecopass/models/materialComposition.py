from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

#TODO: Create material composition model