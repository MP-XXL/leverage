import enum

class Verification(enum.Enum):
    verified = "verified"
    pending = "pending"
    unverified = "unverified"


class AccountStatus(enum.Enum):
    dormant = "dormant"
    active = "active"
    blocked = "blocked"

class TransactionType(enum.Enum):
    credit = "credit"
    debit = "debit"