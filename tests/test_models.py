import pytest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError
from NMIS_Ecopass.models import Metadata, StatusEnum
from NMIS_Ecopass.utils import create_metadata, update_metadata, validate_metadata, generate_uuid

def test_create_metadata():
    metadata = create_metadata(
        economic_operator_id="ECO-123456789",
        issue_date=datetime.now(),
        status=StatusEnum.ACTIVE
    )
    assert metadata.economic_operator_id == "ECO-123456789"
    assert metadata.status == StatusEnum.ACTIVE
    assert validate_metadata(metadata) is True

def test_create_metadata_invalid():
    with pytest.raises(ValidationError):
        create_metadata(
            economic_operator_id="INVALID ID!!",  # Non-alphanumeric should raise an error
            issue_date=datetime.now(),
            status=StatusEnum.ACTIVE
        )

def test_update_metadata():
    metadata = create_metadata(
        economic_operator_id="ECO-123456789",
        issue_date=datetime.now(),
        status=StatusEnum.ACTIVE
    )
    updated_metadata = update_metadata(metadata, status=StatusEnum.EXPIRED)
    assert updated_metadata.status == StatusEnum.EXPIRED

def test_generate_uuid():
    uuid1 = generate_uuid()
    uuid2 = generate_uuid()
    assert isinstance(uuid1, uuid4().__class__)
    assert uuid1 != uuid2

def test_metadata_to_dict():
    metadata = create_metadata(
        economic_operator_id="ECO-123456789",
        issue_date=datetime.now(),
        status=StatusEnum.ACTIVE
    )
    metadata_dict = metadata.dict()
    assert isinstance(metadata_dict, dict)
    assert metadata_dict["economic_operator_id"] == "ECO-123456789"
