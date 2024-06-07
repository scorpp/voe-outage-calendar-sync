import datetime
import hashlib
from dataclasses import dataclass
from enum import Enum


class DisconnectionEnum(str, Enum):
    CONFIRMED = "Confirmed"
    UNCONFIRMED = "Unconfirmed"

    def __str__(self):
        return self.value


@dataclass
class Disconnection:
    start: datetime.datetime
    end: datetime.datetime
    status: DisconnectionEnum

    def id(self):
        digest = hashlib.md5()
        digest.update(self.start.isoformat().encode("utf-8"))
        digest.update(self.end.isoformat().encode("utf-8"))
        digest.update(str(self.status).encode("utf-8"))
        return digest.hexdigest()

    def __str__(self):
        return f"{self.start.isoformat()} {self.end - self.start} {self.status}"
