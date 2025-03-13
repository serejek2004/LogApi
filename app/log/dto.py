from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogDTO:
    created_at: datetime
    log_level: str
    log_data: str

    @classmethod
    def from_request(cls, data):
        return cls(
            created_at=data['created_at'],
            log_level=data['log_level'],
            log_data=data['log_data']
        )
