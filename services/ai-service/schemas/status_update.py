from dataclasses import dataclass
from enum import Enum
from typing import Union, Optional, Dict, Any

from enums.document_status import JobStatus, ResumeStatus

@dataclass
class StatusUpdate:
    status: Union[JobStatus, ResumeStatus]
    id: str
    session_id: str
    additional_data: Optional[Dict] = None
    log_extra: Optional[Any] = None

    def to_message(self) -> Dict:
        message = {
            "Id": self.id,
            "Status": self.status.value,
            "SessionId": self.session_id
        }
        if self.additional_data:
            message.update(self.additional_data)
        return message

    def to_log_extra(self) -> Dict:
        return {
            **(self.log_extra or {}),
            "status": self.status.name,
            "status_code": self.status.value            
        }