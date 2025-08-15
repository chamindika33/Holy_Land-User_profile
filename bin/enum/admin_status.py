from enum import Enum


class AdminStatus(str, Enum):
    PENDING = "pending"
    APPROVE = "approve"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    ARCHIVE = "archive"