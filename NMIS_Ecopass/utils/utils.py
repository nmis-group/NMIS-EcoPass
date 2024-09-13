from typing import Dict, Any, Optional
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import ValidationError, HttpUrl
from ..models import Metadata, StatusEnum

def generate_uuid() -> UUID:
    """Generate a new UUID4 for passport_identifier."""
    return uuid4()

def create_metadata(
    economic_operator_id: str,
    passport_identifier:UUID,
    issue_date: datetime,
    status: StatusEnum,
    backup_reference: Optional[HttpUrl] = None,
    registration_identifier: Optional[HttpUrl] = None,
    last_modification: Optional[datetime] = None,
    predecessor: Optional[str] = None,
    version: Optional[str] = None,
    expiration_date: Optional[datetime] = None
) -> Metadata:
    """
    Create a new MetaData for DPP instance with the provided data.
    
    Args:
        economic_operator_id: The identifier for the economic operator.
        issue_date: The date when the DPP was issued.
        status: The current status of the metadata.
        backup_reference: Optional reference to a backup version of the DPP.
        registration_identifier: URL back to EU Registry.
        last_modification: Timestamp of the last modification to the DPP.
        predecessor: Optional reference to the predecessor version of the DPP.
        version: Internal version of the DPP.
        expiration_date: The date when the DPP will expire, if applicable.

    Returns:
        Metadata: A validated Metadata instance.
    """
    passport_identifier = generate_uuid()
    try:
        metadata = Metadata(
            economic_operator_id=economic_operator_id,
            issue_date=issue_date,
            status=status,
            passport_identifier=passport_identifier,
            backup_reference=backup_reference,
            registration_identifier=registration_identifier,
            last_modification=last_modification,
            predecessor=predecessor,
            version=version,
            expiration_date=expiration_date
        )
        return metadata
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise

def metadata_to_dict(metadata: Metadata) -> Dict[str, Any]:
    """
    Convert a Metadata instance to a dictionary.
    
    Args:
        metadata: The Metadata instance to convert.
    
    Returns:
        dict: A dictionary representation of the Metadata instance.
    """
    return metadata.dict()

def update_metadata(metadata: Metadata, **kwargs) -> Metadata:
    """
    Update an existing Metadata instance with new values.
    
    Args:
        metadata: The Metadata instance to update.
        kwargs: The fields to update.
    
    Returns:
        Metadata: The updated Metadata instance.
    """
    update_data = metadata.dict()
    update_data.update(kwargs)
    try:
        updated_metadata = Metadata(**update_data)
        return updated_metadata
    except ValidationError as e:
        print(f"Validation error during update: {e}")
        raise

def validate_metadata(metadata: Metadata) -> bool:
    """
    Validate a Metadata instance.
    
    Args:
        metadata: The Metadata instance to validate.
    
    Returns:
        bool: True if the metadata is valid, False otherwise.
    """
    try:
        metadata.validate(metadata.dict())
        return True
    except ValidationError as e:
        print(f"Validation failed: {e}")
        return False

def print_metadata(metadata: Metadata) -> None:
    """
    Print the metadata details in a readable format.
    
    Args:
        metadata: The Metadata instance to print.
    """
    print(f"Metadata ID: {metadata.passport_identifier}")
    print(f"Economic Operator ID: {metadata.economic_operator_id}")
    print(f"Issue Date: {metadata.issue_date}")
    print(f"Status: {metadata.status}")
    print(f"Version: {metadata.version}")
    print(f"Expiration Date: {metadata.expiration_date}")
    print(f"Backup Reference: {metadata.backup_reference}")
    print(f"Registration Identifier: {metadata.registration_identifier}")
    print(f"Last Modification: {metadata.last_modification}")
    print(f"Predecessor: {metadata.predecessor}")
