from uuid import UUID
from datetime import datetime


class BaseEntity:
    id: UUID
    created_at: datetime
    updated_at: datetime
