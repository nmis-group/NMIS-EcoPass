from NMIS_Ecopass.utils import generate_uuid,create_metadata
from NMIS_Ecopass.models import Metadata,StatusEnum
from datetime import datetime

passportUUID=generate_uuid()

metadata = create_metadata(
    passport_identifier=passportUUID,
    economic_operator_id="ECO123456789",
    issue_date=datetime.now(),
    status=StatusEnum.ACTIVE)


print(metadata)
